Done. Linter reports no findings (exit 0) in STE-flavored mode.

`outputs/pr_description.md`:

- **What changed** — `internal/net/client.go` retries after a timeout or connection error, with a doubling wait and jitter; retry count and base delay are client options; only idempotent requests repeat.
- **Why** — one try per request turned a brief network problem into a hard failure; backoff keeps a request alive through a short outage.
- **How I tested** — unit tests in `internal/net/client_test.go` for the backoff schedule, the retry cap, and the error classes; a soak test through a fault-injecting proxy that drops connections, delays responses, and returns 5xx codes.
- **Notes** — `net/http` only, no new dependency, no caller changes.

I kept the numbers I could not verify out of the text (no retry count, delay values, or pass metrics). Add them if you want the description to state the exact defaults.