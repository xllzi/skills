Saved to `outputs/pr_description.md`.

The description covers the three requested areas:

- **What changed** — retry loop in `Client.Do` with full-jitter exponential backoff, a defaults table for `MaxAttempts`/`BaseDelay`/`MaxDelay`/`RetryBudget`, the retryable-vs-terminal error split, idempotency guard for POST, body replay rules, `Retry-After` handling, context cancellation during sleep, and new metrics.
- **Why** — the observed 0.4% transient failure rate on lossy paths, plus the two rejected alternatives (call-site retries, `RoundTripper` wrapper) and why `Client.Do` is the right seam.
- **How it was tested** — unit test cases by category, and the 30-minute soak test against a fault-injecting proxy with a control run (0.40% → 0.006% final failures, p99 1.9s → 2.1s, 1.8% extra requests).

Two notes on the draft: the numbers, option names, and metric names are invented, since there were no input files — replace them with the real values before posting. I also added a risk/rollout section and checklist beyond what you asked for; drop them if the repo's PR template doesn't use them.