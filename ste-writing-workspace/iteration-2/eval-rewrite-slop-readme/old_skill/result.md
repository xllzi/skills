Rewrote the README in STE-flavored mode and saved it to `outputs/readme.md`. The linter reports `no findings`.

What changed:

- **Cut the marketing adjectives** — cutting-edge, robust, seamlessly, revolutionary, next-generation, powerful, world-class, effortlessly, unparalleled, blazing fast, enterprise-grade, comprehensive.
- **Cut the slop phrasing** — "It's important to note that", "In order to", "Additionally/Furthermore/Moreover", "empowers teams to leverage", "perform an installation of", "commence discovering ... prior to".
- **Removed contractions** and the em dash (split into two sentences).
- **Active voice** — "The collector reads logs from each host" instead of "The logs are ingested by the collector".
- **Kept every factual claim**: pipeline with collector + transformation engine, one view across the stack, install the agent per host, it finds log sources and ships them, no configuration, dashboard, fast queries, the three feature bullets.

```markdown
# Logboat

Logboat collects logs from your systems and stores them in one place.

## How it works

The pipeline has two stages. The collector reads logs from each host. The
transformation engine then processes them. You get one view of the activity
across your stack.

## Install

1. Install the agent on each host.

The agent finds the log sources on the host and sends the logs to Logboat. It
does not need configuration.

## Dashboard

The dashboard shows your log data. Queries are fast.

## Features

- Connects to more than 50 tools
- Security for enterprise use
- Scales to petabytes
```

One judgment call worth flagging: "blazing fast" and "effortless scaling" were unsupported puffery, so I rendered them as plain claims ("Queries are fast", "Scales to petabytes") rather than deleting them. If the speed claim has no benchmark behind it, drop that sentence entirely.