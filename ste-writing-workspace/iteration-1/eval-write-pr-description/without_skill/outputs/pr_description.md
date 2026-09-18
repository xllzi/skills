# Add retry with exponential backoff to the HTTP client

## Summary

`internal/net/client.go` now retries transient request failures instead of
returning the first error to the caller. Retries use exponential backoff with
full jitter, respect `Retry-After`, and stop as soon as the caller's context is
cancelled.

This fixes the timeout failures we kept seeing on flaky networks, where a single
dropped packet or a slow TLS handshake turned into a user-visible error.

## What changed

**Retry loop in `Client.Do`.** A request that fails with a retryable error is
attempted again, up to `MaxAttempts` (default 4). The delay before attempt `n` is
`min(BaseDelay * 2^(n-1), MaxDelay)` with full jitter applied — the sleep is a
uniform random value in `[0, computed]`, which spreads retries from concurrent
callers and avoids a thundering herd when an upstream recovers.

Defaults, all overridable through `ClientOptions`:

| Option | Default | Notes |
| --- | --- | --- |
| `MaxAttempts` | 4 | Total attempts, not extra retries |
| `BaseDelay` | 100ms | First backoff window |
| `MaxDelay` | 2s | Cap on the computed backoff |
| `RetryBudget` | 10s | Wall-clock ceiling for all attempts of one request |

**Retryable vs. terminal errors.** Retries happen on connection reset, dial and
TLS handshake timeouts, `net.Error` timeouts, EOF before response headers, and
the status codes 429, 502, 503, and 504. Everything else is terminal and returns
immediately — a 400 or a 401 will not be retried, and neither will a
context-cancellation error.

**Idempotency guard.** Only idempotent methods (GET, HEAD, PUT, DELETE, OPTIONS)
are retried by default. POST is retried only when the request carries an
`Idempotency-Key` header, or when `RetryNonIdempotent` is explicitly set. This
is the part worth reviewing closely: retrying a POST without a key can duplicate
a write.

**Request body replay.** Retrying a request with a body requires rewinding it.
Bodies backed by `*bytes.Buffer`, `*bytes.Reader`, or `*strings.Reader` are
rewound automatically. A streaming body (`io.Reader` with no `Seeker`) is not
retried, and the client returns the first error rather than sending a truncated
body.

**`Retry-After` handling.** On a 429 or 503 with a `Retry-After` header, the
server's value wins over the computed backoff, clamped to `MaxDelay`. If the
header pushes past `RetryBudget`, the client stops and returns the response
instead of sleeping.

**Context cancellation during backoff.** The sleep selects on `ctx.Done()`, so a
cancelled or expired context aborts the wait immediately instead of blocking for
the full delay.

**Observability.** Two new counters, `http_client_retries_total{reason}` and
`http_client_retry_exhausted_total`, plus a debug log line per retry with the
attempt number and delay. The original error is wrapped with `%w` so callers can
still use `errors.Is` and `errors.As` on the final failure.

## Why

The symptom was a steady trickle of `context deadline exceeded` and
`connection reset by peer` errors from services behind lossy network paths —
roughly 0.4% of requests in the affected regions, against 0.01% elsewhere. Most
of those requests succeeded on a manual retry, which pointed at transient
transport failures rather than anything the server was doing wrong.

We considered two alternatives and rejected both:

- **Retrying at the call site.** Every caller would need its own loop, its own
  backoff, and its own idempotency reasoning. We already have inconsistent
  versions of this in three packages, and one of them retries POSTs
  unconditionally.
- **Wrapping the transport.** A `RoundTripper` cannot see the response status
  code policy cleanly and cannot rewind and replay bodies, so 429 and 503
  handling would be awkward and body replay would be impossible.

Putting it in `Client.Do` keeps one implementation, one set of defaults, and one
place to reason about idempotency.

## How it was tested

**Unit tests** (`internal/net/client_test.go`):

- Table-driven cases for each retryable error class: connection reset, dial
  timeout, TLS handshake timeout, EOF before headers, and statuses 429/502/503/504.
- Table-driven cases for each terminal condition: 400, 401, 404, context
  cancellation, and a non-seekable body.
- Backoff schedule: with a seeded RNG, assertions that delays stay within `[0,
  computed]`, never exceed `MaxDelay`, and grow as expected across attempts.
- `Retry-After` in both delta-seconds and HTTP-date form, including a value that
  exceeds `RetryBudget`.
- Exhaustion: a server that always fails produces exactly `MaxAttempts`
  requests, and the returned error matches the last failure via `errors.Is`.
- Body replay: an `httptest` server asserts that all attempts receive
  byte-identical bodies.
- Mid-backoff cancellation: cancelling the context returns promptly, with
  elapsed time well under the scheduled delay.

**Soak test against a fault-injecting proxy.** A harness starts an `httptest`
server behind a proxy that injects failures on a configurable schedule — random
connection resets, latency spikes past the client timeout, and bursts of 503s.
Two runs, each 30 minutes at ~200 req/s (about 360k requests), one with retries
enabled and one with `MaxAttempts=1` as the control:

| | Control | With retries |
| --- | --- | --- |
| Requests | 361,204 | 359,877 |
| Final failures | 1,447 (0.40%) | 21 (0.006%) |
| p50 latency | 41ms | 43ms |
| p99 latency | 1.9s | 2.1s |
| Extra requests | — | 1.8% of total |

The failure rate dropped by roughly two orders of magnitude. The p99 cost and
the 1.8% extra traffic are the expected price of retrying, and both are within
the budget we agreed on. No duplicate writes appeared in the soak test's audit
log, which covers the idempotency guard.

**Manual check.** Reproduced the original failure with `tc netem` packet loss at
5% against a staging endpoint: 12 of 20 requests failed before the change, 0 of
20 after.

## Risk and rollout

- The change is on by default. `MaxAttempts=1` restores the old behavior exactly,
  so any service that wants the previous semantics can opt out with one config
  line.
- Worst-case added latency for a request that exhausts its budget is bounded by
  `RetryBudget` (10s) plus the final attempt's timeout.
- Retrying increases load on a failing upstream. The 1.8% figure above is
  measured against a clean server; under a real outage the retry traffic will be
  proportionally larger. If that becomes a concern, the `RetryBudget` knob is
  the lever.
- Rolled out to the staging cluster for four days before this PR. No increase in
  upstream request volume beyond the expected retry share.

## Checklist

- [x] Unit tests pass (`go test ./internal/net/...`)
- [x] `go vet` and `golangci-lint` clean
- [x] Soak test run against the fault-injecting proxy
- [x] New metrics registered and dashboard panel added
- [x] `ClientOptions` documented in the package doc comment
