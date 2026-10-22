---
name: zvec-grep
description: Search local workspace code, documents, configuration, and data with zg (zvec-grep). Use for project understanding, semantic discovery, tracing relationships, and cross-file synthesis, while the index is present or user explicitly tell you to use zg. 
---

# zvec-grep

Choose the evidence source before the retrieval mode. Use the available zvec-grep MCP tools, or the installed `zg` CLI when MCP search is unavailable.

## Workspace evidence

- Use the current workspace when the user asks about local material, prior context establishes it as relevant, or the question concerns how the current project works—even if the workspace is not mentioned explicitly.
- A workspace may mix code, documents, configuration, and data. An incidental or negative mention of a workspace does not make it the evidence source.
- Do not use workspace retrieval for unrelated open-world questions, current external facts, or web content that does not depend on local evidence.
- Resolve the intended workspace to an absolute path. Pass a daemon-visible absolute `root` on every zvec-grep MCP workspace call. For CLI calls, set the execution tool's working directory to that absolute root; do not invent a `--root` flag or assume a remote daemon shares local paths.

## Retrieval routing

| Task | Route |
| --- | --- |
| A known exact word, phrase, name, date, identifier, filename, path, configuration key, error, source fragment, literal, or regex; locating occurrences is sufficient | `zvec_grep_rg` when listed by the current host; otherwise native Grep or `rg` |
| Unknown wording or location; semantic, conceptual, fuzzy, or paraphrase discovery | `zvec_grep_search` |
| Relationships, chronology, causality, architecture, data/control flow, comparison, or synthesis across files or sections | `zvec_grep_search` |
| Exact anchors plus relationships or cross-file synthesis | Search with the concept and anchors first, then focused `zvec_grep_rg` or native Grep/`rg` |

- When MCP search is unavailable, use the corresponding indexed CLI search described below, subject to the same index authorization rules.
- If no sufficient exact anchor exists and the user asks whether conceptually related material exists locally, make **at most one focused semantic probe** using the question plus distinctive names, dates, or terms. Continue only if results are relevant; otherwise report that the indexed workspace did not establish the answer. This limit does not apply to exact quotations, configuration keys, filenames, regexes, or exhaustive occurrence requests.
- Search before broad file reads or delegating workspace discovery. Do not delegate solely to locate material. Stop when evidence is sufficient.
- Ranked lexical search (`fts` / `--fts`) is not exhaustive grep, and lexical anchors are not hard filters. For filenames, use filename discovery such as `rg --files -g 'pattern'`; content matching alone does not locate filenames reliably.

## MCP calls

Use the actual tool names and schemas exposed by the host; names may have namespace prefixes. Do not assume `zvec_grep_rg` is available or change the server toolset just to obtain it.

Conceptual search, with optional lexical anchors for a mixed task:

```json
{
  "root": "/absolute/path/to/workspace",
  "query": "how expired sessions reach the login redirect",
  "fts": ["SessionStore", "redirectToLogin"],
  "fuse": true,
  "limit": 5
}
```

Omit `fts` and `fuse` when no useful anchors exist. Scope with `globs` or `fileTypes` when the relevant area is known. Add only parameters supported by the current tool schema.

Exact follow-up when `zvec_grep_rg` is listed:

```json
{
  "root": "/absolute/path/to/workspace",
  "command": "rg -n -F 'redirectToLogin' src"
}
```

## CLI fallback

Read `zg --version` and `zg --help` once when the installed interface is unknown. Follow installed help: version 0.2.2 uses subcommands, while upstream main documents positional search and long action options. Do not blindly retry one syntax as another: newer versions may treat old command words as query text.

Run these examples from the resolved absolute workspace root, **only with an existing index or explicit authorization to create one**:

```sh
# Subcommand interface: verify options with zg query --help.
zg query 'how expired sessions reach the login redirect' --preview short --limit 5
zg query --hybrid 'session expiration flow' --fts 'SessionStore' --fuse --preview short --limit 5

# Positional interface: verify options with zg --help search.
zg 'how expired sessions reach the login redirect' --preview short --limit 5
zg --hybrid 'session expiration flow' --fts 'SessionStore' --fuse --preview short --limit 5
```

Use just the matching interface. Request snippets explicitly because CLI pipe output may omit them. Exact fallback remains native Grep/`rg`; if the user specifically requests managed CLI grep, use `zg query --rg` or `zg --rg` according to installed help. Managed grep needs no index; use native `rg` for filename discovery or output modes the wrapper rejects.

If neither MCP search nor the CLI is available, state the limitation. Use focused native search where sufficient; do not silently install software or imply semantic retrieval ran.

## Search evidence

- Bounded source snippets count as already-read evidence. Read a cited file only when required details fall outside the snippet or freshness affects the conclusion; read the relevant region rather than the whole file.
- Cite source paths and available line ranges or section locations. Distinguish direct evidence from inferred relationships.
- Ranked results and empty searches do not prove exhaustive absence. State the scope of the evidence, especially when files may be ignored, excluded, unsupported, or stale.

## Freshness and index lifecycle

- Read `freshness` and `background_refresh` from search results without a status preflight. `served_from_current_index` describes where results came from, not a guarantee that they are fresh. Use sufficient current-index results without waiting for background refresh.
- If results are possibly stale and the task depends on current content, verify the relevant source or request fresh results using the supported freshness option. Do not poll status routinely.
- Creating, rebuilding, or dropping a persistent index requires an explicit user request or authorization. A request to search is not authorization to create an index.
- **Prevent implicit creation too.** Some CLI versions create an index on the first indexed query. Before using an interface that can do this, establish that an index already exists from known context or a read-only check of `<root>/.zvec-grep/manifest.json`. A directory alone is insufficient. If metadata is missing or invalid, do not issue an indexed query that could create or repair it; use exact lookup where sufficient or ask for index creation authorization. Do not use a routine status preflight as a substitute.
- If the index is missing but exact/regex lookup can answer the task, use `zvec_grep_rg` when listed, otherwise native Grep/`rg`. If semantic retrieval is essential, explain the missing prerequisite and request authorization only for the required operation.
- Respect existing remote-embedding authorization. Do not add `--allow-remote`, grant persistent access, switch models, or change integrations merely to bypass a retrieval error. Honor authorization already given for the intended scope.

## Upstream references

Consult these when installed help or exposed schemas leave a relevant detail unresolved:

- [CLI guide](https://github.com/zvec-ai/zvec-grep/blob/main/docs/02-cli.md)
- [MCP guide](https://github.com/zvec-ai/zvec-grep/blob/main/docs/03-mcp.md)
- [Index scope and retrieval pipeline](https://github.com/zvec-ai/zvec-grep/blob/main/docs/04-pipeline.md)
