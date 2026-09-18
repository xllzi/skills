# Add retry logic with exponential backoff to the HTTP client

## What changed

The HTTP client in `internal/net/client.go` retries a request after a
timeout or a connection error. The client waits before each new try, and
the wait doubles after each failure. A small random delay, or jitter,
goes on top of each wait. The jitter stops many clients from a retry at
the same moment.

The retry count and the base delay are options on the client. The client
uses the default values when the caller sets nothing.

The client retries only idempotent requests. It does not retry a POST
with a body, unless the caller marks the request idempotent.

## Why

On flaky networks, a request failed after one try with a timeout. A
short network problem then became a hard failure for the caller. Users
saw these timeouts often, and each timeout lost a unit of work.

Retries with backoff keep a request alive through a brief outage. The
retry count and the base delay set the limit on the extra latency.

## How I tested

Unit tests in `internal/net/client_test.go` cover three areas:

- The backoff schedule. The tests check the wait time for each try.
- The retry count. The tests check that the client stops at the limit.
- The error classes. The tests check that a 4xx response stops the
  retry and that a timeout starts it.

The soak test sends traffic through a proxy that injects faults. The
proxy drops connections, delays responses, and returns 5xx status codes
at random. The test confirms that the client recovers from each fault
type, and that the transport stays healthy after the faults stop.

## Notes

The change uses `net/http` only, with no new dependency. The retry logic
stays inside the client, so callers need no changes.
