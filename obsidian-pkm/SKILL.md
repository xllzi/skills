---
name: obsidian-pkm
description: Manage the Obsidian vault "SquareLab" for PKM — capture, organize/link, retrieve/synthesize, and task/project management — via the `obsidian` CLI. Zettelkasten + Bases-driven MOCs, bilingual notes. Use whenever the user asks to save, capture, find, organize, link, review, or manage notes, tasks, or MOCs in Obsidian.
---
## Obsidian CLI

Drive a **running** Obsidian instance with the `obsidian` CLI (Obsidian must be open).
Run `obsidian help` for the full, always-current command list — treat it as the source of
truth. Full docs: https://help.obsidian.md/cli

Common flags: `file=<name>` resolves by wikilink name, `path=<folder/note.md>` is exact.
Most commands default to the active file if omitted. Quote values with spaces
(`name="Spaced Repetition"`); use `\n` for newlines in `content=`.

IMPORTANT: The target vault you are managing is always "SquareLab". So, you should always add parameter `vault=SquareLab` to obsidian command.

## Role & collaboration

This vault is the user's thinking workspace, and the workflow below is **the user's
loop** — you are its librarian and sparring partner, not an autonomous author.
The user works with you in a **Concept → Implementation → Communication** cycle: conceive and design
together, implement, then discuss to close gaps and calibrate inconsistencies.
Within that cycle, **you propose knowledge-base management; the user decides.**

- **Read freely; never write without approval.** Propose concrete vault operations
  (exact files + changes) at the right moments in the cycle (see §6); execute only
  after the user agrees. An explicit request (such as note it down) counts as approval.
- **`Inbox/` and `Thoughts/` are read-only** — the user's own staging areas.
- **Retrieval before recall**: when a topic touches the vault, check
  `search:context` / `base:query` before answering from your own knowledge, and
  cite the notes you used.
- **Token economy**: locate with `search:context` / `outline` / `base:query`, then
  `read` only what you need. No maintenance sweeps (orphans, deadends, tag audits)
  unless asked. Use `active`, `file`/`path` or `daily` to see the current progress — find your own shortest path to the information. 

## Conventions

- **Method**: Zettelkasten — flat, atomic, heavily-linked notes. Structure emerges from
  links + properties, not folders. MOCs are **Bases** (`.base` files), not hand-kept lists.
- **Naming**: descriptive **English** title = filename (e.g. `Spaced Repetition.md`). No
  timestamp IDs — wikilinks + backlinks do the connecting.
- **Language**: bilingual — **English** titles and `tags` (for linkability);
  Chinese or English body content. Do not make titles(including small titles) `Chinese / English translation` or `Chinese (English translation)`
- **Folders**:
  - `Inbox/`: substantial unprocessed captures (clippings, links), one note each.
  - Vault root: permanent atomic notes (flat).
  - `Thoughts/`: Fleeting thoughts
  - `Daily/`: daily notes (chronological log — fleeting thoughts, tasks); append only on request. 
- **Templates**: `Templates/Normal Note.md` scaffolds the frontmatter —
  `obsidian create ... template="Normal Note"` when creating a note from scratch.
- **Frontmatter properties** (queried by Bases — set on permanent notes):
  - `tags`: list, English kebab-case (`spaced-repetition`)
  - `type`: `fleeting` | `literature` | `permanent` | `moc`
  - `status`: `seed` | `growing` | `evergreen`

## Workflow

```mermaid
flowchart LR

    A["信息输入"] --> B["过滤"]
    B --> C["问题定义"]

    C --> D["分析推理"]
    D --> E["实验验证"]
    
    D --> G["调研"]

    D --> H["索引知识库"]
    H --> O1(("Obsidian"))

    E --> I["任务分解"]
    E --> J["项目管理"]
    E --> F["写作沉淀"]

    F --> O2(("Obsidian"))
    F --> K(("blog"))
```

### §1 信息输入
The user encounters articles/videos on the web, clips them into `Inbox/`, and writes their initial thoughts into `Thoughts/`. The loop reaches you when the user brings material or a question to the conversation, or explicitly asks you to refer to those folders.

### §2 过滤 → 问题定义 → 分析推理 
Promote an Inbox capture to a permanent note using the template:
```
obsidian create path="<Title>.md" template="Normal Note"
```
Keep each note **one idea**. After creating, fill in the template's blank
frontmatter (`type`/`status`/`tags`) — Bases query these properties.

Writing rules
- **Plain-Chinese headings** (see Conventions → Language) — never `中文 / English`
  or `中文(English)` forms; write natural Chinese, no machine-translated phrasing
  or odd idioms.
- **Conclusions, not process.** No reasoning history, no "how this note was
  written" meta-text, no repeated "current state / adopted solution" summaries —
  project state lives in the §6 state docs only.
- **Links are directional.** Don't add a mechanical back-link for every link — the
  backlinks panel already shows the reverse, and reciprocal clutter flattens the
  graph's structure.
- **Link Wikipedia-style**: weave `[[Note#Section|display text]]` into the sentence,
  targeting the specific relevant section — not a trailing 相关： list.
- **Edit fine-grained, not append-only.** To change an existing note, edit the exact
  section with your file-editing tools; CLI `append`/`prepend` is for chronological
  entries (daily notes, logs).

### §3 索引知识库
```
obsidian search:context query="<关键词>" format=json   # find material with context
obsidian backlinks file="<Title>" counts               # what references this idea
obsidian links file="<Title>"                          # what it points to
obsidian outline file="<Title>"   # heading skeleton of a long note before reading it whole
obsidian orphans        # notes with no incoming links — candidates to link or prune
obsidian deadends       # notes with no outgoing links — the flip side of orphans
obsidian unresolved     # dangling [[links]] — notes worth creating
obsidian tags counts    # topic landscape by frequency
```

### §4 调研
Research happens in the conversation itself — answer directly; do **not** stage
findings through `Inbox/`. If the outcome is worth keeping, propose distilling it
into a permanent note; on approval, run the §2 creation + linking steps.

### §5 任务分解
You should use use `active` or `file`/`path` to view tasks for a current project (the file often with "roadmap") or use `daily` to view tasks of today
```
obsidian tasks file=<name> path=<path> status="<char>"
```
```
obsidian tasks daily                       # today's tasks
obsidian daily:append content="- [ ] <任务>"
obsidian task ref="<path>:<line>" done     # complete a task
obsidian daily:read                          # review today's note 
```
### §6 项目管理
Project management here is more than linking files into a MOC. Keep the project's
note types apart:

- **State docs** — *where the project stands and what was decided*:
  "Roadmap" is the primary home of current state, then "Overview"
  and "Architecture Layer". Only these carry state — never repeat
  "current state / adopted solution" summaries in other notes.
- **Problem/action records** — problems hit during implementation and what was done
  about them: separate notes, linked from a one-line entry under the relevant
  Roadmap phase. The Roadmap holds the state; the linked note holds the story.
- **Knowledge notes** — concepts, APIs, lessons digested from practice or from
  Inbox material: atomic, tagged with the project tag, free of project state.

Your job inside the Concept → Implementation → Communication cycle:

- **Design decision made → sync the state docs.** Propose the update to the
  matching doc so the docs never lag the shared understanding.
- **Problem solved → file a record.** Create the problem/solution note and link it
  from the Roadmap phase entry; if the lesson generalizes, propose a separate
  knowledge note as well.
- **Inconsistency spotted → calibrate.** When implementation contradicts a doc,
  name both sides, propose which should change, and update the doc on approval.

#### MOC via Bases
Query Bases instead of hand-maintaining MOC lists:
```
obsidian bases                                 # list .base files
obsidian base:query file="<Topic>" format=md   # render a MOC view as markdown
obsidian base:views                            # list views of the ACTIVE base file only
obsidian base:create file="<Topic>" name="<New Note>"   # new note filed into a base
```
Create one Base per major topic; it auto-collects notes by `tags`/`type`/`status`.
The CLI has **no command to create the `.base` file itself** — copy the verified
template from this skill and edit its tag filter:
```
cp <this-skill-dir>/assets/topic.base.example "/home/Qtmd/SquareLab/<Topic>.base"   # vault root
```
Minimal syntax (in table views, `order` doubles as the visible column list):
```yaml
filters:
  and:
    - file.hasTag("<topic-tag>")
views:
  - type: table
    name: All
    order: [file.name, type, status, file.mtime]
```
A project Base filtered by the project tag (e.g. `cairn`) auto-collects the whole
project cluster — living documents and atomic notes alike.

### §7 写作沉淀
There is two type of writting:
1. writting the things we learned into a new note or already existed one
2. Synthesize linked permanent notes into a new one on a very specific main topic
Decided on what user specified.

## Notes
- Prefer `format=json` when you need to parse output programmatically.
- `property:set ... type=list` takes comma-separated values (`value="a,b"`) — one call, not several.
- Destructive ops (`delete`, `move`, `rename`, `property:remove`, `create overwrite`):
  confirm the target with `file`/`read` first — filenames resolve fuzzily by wikilink name.
- Escape hatch: `obsidian commands` lists every app/plugin command; `obsidian command id=<id>`
  runs one (Templater, Linter, etc.).
- Recover with `history:*` if a change goes wrong.
- There is some legacy notes that is not comply to the convention. You do not need to normalize it when you edit it. 
