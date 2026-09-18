Linter passes clean — zero errors, zero warnings in STE-flavored mode.

**Saved to:** `/home/Qtmd/skills/ste-writing-workspace/iteration-1/eval-rewrite-slop-readme/with_skill/outputs/readme.md`

What I changed and why:

- **Cut the marketing adjectives** (`cutting-edge`, `robust`, `seamless`, `revolutionary`, `next-generation`, `powerful`, `world-class`, `effortless`, `unparalleled`, `enterprise-grade`, `blazing`). The linter flags these as W03; they also carry no information.
- **Cut the empty framing** — "empowers teams to leverage their log data like never before" and "It's important to note that" say nothing. The pipeline description now states directly what the collector and transformation engine do.
- **Killed the AI-tell transitions** — "Additionally / Furthermore / Moreover / In order to / prior to / commence". Three "also"-style connectors in a row were the loudest slop signal in the original.
- **Active voice throughout.** "The logs are ingested by the collector" became "The collector gathers logs on each host".
- **Made the install section an actual procedure** — a numbered list, one action per item, which is what a reader wants there.

Two judgment calls worth flagging, since a rewrite should not invent facts:

- "Robust, enterprise-grade security" and "Effortless scaling to petabytes" had no measurable content. I kept the underlying claims but stated them flatly ("Has security controls for enterprise use", "Scales to petabytes") rather than deleting the feature bullets or inventing specifics like encryption or replication numbers.
- "It's blazing fast" became "it processes logs quickly" — same claim, no puffery. If you have a real throughput or latency figure, that line is much stronger with the number in it.