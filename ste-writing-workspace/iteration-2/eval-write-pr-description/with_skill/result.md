Saved to `outputs/pr_description.md`. The linter reports no findings (exit 0), and manual checks confirm: 274 words, longest sentence 20 words, no em/en dashes, no contractions, no passive voice.

The document has three sections:

- **What changed** — retry on timeout and temporary network errors, no retry on 4xx, plus the retry policy values and the stop conditions (good response, 4xx, canceled context).
- **Why** — the flaky-network timeouts, the manual retries and user-visible errors they caused, and the server-protection argument for the growing delay.
- **How tested** — unit tests with a fake clock covering each error type, the delay sequence, the attempt cap, and cancellation; soak test against a fault-injecting proxy for `<soak duration>`.

The task gave no retry numbers, test file names, or run results, so the document uses angle-bracket placeholders (`<max attempts>`, `<base delay>`, `<test file>`, `<failure count>`, `<artifact link>`). Each placeholder names what fills it. Replace them before you post the PR.