Saved to `outputs/pr_description.md`. The linter reports no findings (STE-flavored mode, `python3 scripts/ste_lint.py`).

Two warnings from the first pass were checked and resolved:
- V01 `'is canceled'` — real passive voice. Rewrote as "when the caller cancels the context".
- S04 on the test list — the heuristic flagged `after` in "The attempts stop after `MaxRetries`". That item is a statement, not a step, so the rule does not apply. Reworded to "stop at `MaxRetries`" to keep the list clean.

The document covers the retry policy (4 attempts, 100/200/400/800 ms waits, 20 percent jitter), the idempotent-method limit, the retry triggers, the `ClientOptions` knobs, the reason (transient failures on flaky networks), the 6 unit cases, and the 6 hour soak test against the fault-injecting proxy (4.8 percent to 0.02 percent error rate, p99 +340 ms).