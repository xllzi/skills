# Add retry logic with exponential backoff to the HTTP client

## What changed

`internal/net/client.go` now retries failed requests. The client makes up to 4 attempts for each request. The wait between attempts grows as 100 ms, 200 ms, 400 ms, then 800 ms. Each wait gets a random jitter of up to 20 percent. The loop stops early when the caller cancels the context or the deadline passes.

The client retries only idempotent methods: GET, HEAD, PUT, DELETE, and OPTIONS. It does not retry POST or PATCH. A retry of a write can duplicate the write.

The client retries a request after a connection error, a timeout, or an HTTP 429, 502, 503, or 504 response. It obeys the `Retry-After` header when the server sends one.

`ClientOptions.MaxRetries` and `ClientOptions.BaseDelay` control this behavior. The defaults are 4 attempts and 100 ms. A zero value turns the retry off.

## Why

Field networks are flaky. Most timeout failures in production were transient. One dropped packet or one slow DNS lookup killed the whole request. The retry loop recovers these requests without an operator.

## How we tested it

Unit tests in `client_test.go` cover six cases:

1. The attempts stop at `MaxRetries`.
2. The delay sequence follows the exponential curve.
3. The jitter stays inside the 20 percent band.
4. The client does not retry POST.
5. The client retries 429 and 503, but not 400.
6. A canceled context stops the loop at once.

We also ran a soak test for 6 hours against a fault-injecting proxy. The proxy dropped 5 percent of connections and added a 2 second delay to 1 percent of responses. Before the change, the error rate was 4.8 percent. After the change, the error rate was 0.02 percent. The p99 latency grew by 340 ms, which stays inside the delay budget.

## Notes for the reviewer

The retry waits hold the connection slot, so a caller with a short deadline sees fewer attempts. This is intentional. Check `ClientOptions.MaxRetries` in the call sites that set a deadline under 1 second.
