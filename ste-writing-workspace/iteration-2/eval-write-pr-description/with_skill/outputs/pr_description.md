# Add retry logic with exponential backoff to the HTTP client

## What changed

`internal/net/client.go` now retries failed requests with exponential backoff.

The client retries a request when the error is a timeout or a temporary network error. It does not retry after a 4xx response. A retry cannot correct a bad request.

The change sets these retry values:

- Maximum attempts: `<max attempts>`
- Base delay: `<base delay>`
- Backoff factor: `<backoff factor>`
- Maximum delay: `<max delay>`

A good response or a 4xx response stops the loop at once. A canceled context also stops the loop, so a caller keeps control of the wait.

## Why

Timeout failures on flaky networks stopped requests that a second try would have completed. Each failure needed a manual retry, or it reached the user as an error. The backoff absorbs a short network problem, and the caller code does not change.

The growing delay also protects the server. A client that retries at once adds traffic to a server that is already slow. The pause between attempts gives the network time to recover.

## How tested

Unit tests. `<test file>` covers the retry decision for each error type, the delay sequence, the attempt cap, and the canceled-context path. The tests use a fake clock, so they do not wait in real time.

Soak test. A fault-injecting proxy dropped and delayed packets for `<soak duration>` while a client sent a steady stream of requests. The run before the change gave `<failure count>` failures. The run after the change gave `<failure count>` failures. The proxy log and the client log from both runs are in `<artifact link>`.
