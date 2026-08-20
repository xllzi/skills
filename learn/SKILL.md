---
name: learn
description: Personalized learning in the Obsidian vault "SquareLab" — planning, resource finding/verification, quiz-gated practice — so the user spends effort on thinking and practice, not logistics. Slash-invoked only.
disable-model-invocation: true
argument-hint: "<topic> to start or resume; empty lists active topics"
---

## Purpose

Remove learning logistics — planning, finding resources, verifying them, tracking progress — so the user's effort goes to thinking and practice. All state lives in the vault under `Learning/<Topic>/`. Artifacts are streamlined data: YAML frontmatter + markdown tables, never prose.

Primary domains are CS and AI: mechanical exercise checking (run code/tests) is the default.

## Invocation

- `/learn <topic>` — resume `Learning/<topic>/` if it exists, else start a new topic.
- `/learn` — list active topics, one line each: topic, current unit, review-due concepts.
- Plain requests inside a session: "quiz me", "review", "find resources for X", "replan".

## Engine: self-bootstrapping learning loop

Each unit is one bounded real problem, not a lecture:

```
scaffold → predict/attempt → expose gap → teach on demand → verify → distill
```

Practice precedes exposition. Scaffolds fade: early units get worked examples and hints; later units get the problem statement only. The user's theory: vault note `Self-Bootstrapping Learning Loop.md`.

## State

`Learning/<Topic>/` — `<Topic>` is dash-case English. Copy the templates from `<this-skill-dir>/templates/` when creating a topic directory:

| File | Holds |
|------|-------|
| `CURRICULUM.md` | goal, coarse map of all units, detailed plan one step ahead |
| `PROGRESS.md` | mastery per concept + session log (compact table) |
| `RESOURCES.md` | candidate pool + promoted resources |
| `practice/` | saved quizzes, exercises, scratch code. A large repo lives in a sibling directory, linked from here |

Update these after every session and every mastery change. Data, not narrative. No `sessions/` directory; history is the table in PROGRESS.md.

## Starting a new topic

1. Interview briefly: one-line goal, prior knowledge, deadline if any. Fill CURRICULUM.md frontmatter.
2. Draft the coarse map: the unit table. Coarse on purpose — detail only the first unit.
3. Diagnostic quiz, max 10 questions spanning the map. Save as `practice/q000-diagnostic.md` with an answer key. Grade it; label initial mastery per concept in PROGRESS.md.
4. Teach the first unit.

## Session start (resume)

1. Read CURRICULUM.md and PROGRESS.md.
2. Compute review-due concepts: `next-review <= today`. Interval from `last-exposed`, by level: none/partial = 2 days, solid = 7 days, fluent = 21 days.
3. If anything is due, open with a short re-quiz (3–5 questions, reuse saved quizzes from `practice/`) and update mastery first.
4. Then present the next concrete action. Never open a session with "let's plan".

## Unit loop

1. **Pre-unit quiz** (short). Gates: <60% → `none`, reteach with heavier scaffold; 60–85% → `partial`, proceed normally; ≥85% → `solid`, skip exposition, go straight to a harder problem.
2. Present the bounded real problem with the planned scaffold.
3. The user predicts and attempts; expose gaps.
4. Teach on demand — only what the gap needs, citing promoted resources.
5. Verify with a graded exercise:
   - Mechanical checking first: write runnable tests/scripts and execute them.
   - Agent-graded free-form only where mechanical checking is impossible.
   - Multiple-choice only as a warm-up tier.
6. Record: mastery row and session row in PROGRESS.md.
7. `fluent` requires BOTH a delayed re-quiz pass and applying the concept in a new problem. Never grant it on first exposure.

## Resources

Verification is the point; hallucinated or mismatched resources are the failure this skill exists to kill.

- **Pool** (medium check): fetch the URL; confirm it exists and matches its claimed title/description.
- **Promotion** (heavy check): fetch + sample the content + check currency (dates, versions) + assess difficulty against recorded mastery in PROGRESS.md. Only promoted resources appear in teaching.
- RESOURCES.md keeps 1–2 curated picks per unit, one-line verdict each (trust, level fit).
- No trustworthy resource found → teach from parametric knowledge explicitly flagged `UNVERIFIED`; use for exposition only, never cite as a source.

## Distillation

At milestones only (unit or topic completion) and only when an insight generalizes: propose a permanent note at the vault root — English title, frontmatter `tags`/`type`/`status`, links to related notes. Create it only after the user approves: via the `obsidian` CLI when Obsidian is running, otherwise write the file directly at the vault root. Never initiate distillation outside milestones.

## Language

Metadata is English: filenames, frontmatter, table headers, concept names. Teaching language follows the topic and is not compulsory.

## Gotchas

- The vault is **SquareLab** at `/home/Qtmd/SquareLab`. `Learning/` does not exist until the first topic creates it.
- The `obsidian` CLI needs a **running Obsidian app**. If it fails or is absent, work on vault files directly by path; propose before writing.
- Mastery state has one source of truth: the PROGRESS.md table. Never repeat or contradict it in CURRICULUM.md or chat summaries.
- Quiz filenames are the reuse index (`practice/qNNN-<name>.md`, `NNN` increments). Renaming or overwriting a quiz file breaks spaced re-quizzing.
- Never present a resource you did not fetch in this session. A remembered URL is a hallucination candidate until the medium check passes.
