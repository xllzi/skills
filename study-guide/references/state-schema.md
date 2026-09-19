# Cross-session state

Store durable learning state in `.study-guide/STATE.md` in the current project. Create the directory only when a sustained learning goal exists.

Treat the file as a decision-relevant snapshot, not a session log. Preserve the required headings below. Add an optional section only when it contains durable information that changes a future teaching decision.

Use this compact structure:

```markdown
# Study state

## Goal
- Outcome: one observable capability, not a topic name
- Why it matters:

## Current loop
- Problem:
- Next learner action: one observable action
- Mode: exploration | practice | verification | review | transfer
- Verification target:
- Latest result: not run | pass | fail — observation

## Evidence
- Can do independently:
- Can do with a hint:
- Not yet demonstrated:

## Misconceptions and gaps
- [ ] misconception or missing prerequisite — evidence — next check

## Scaffolding
- Current source:
- Current support for the next action: use the support ladder in SKILL.md
- Removal condition:

## Review and transfer
- Review when:
- Transfer task:
- Open questions:
```

For project-based learning, add `## Artifact status` only when verified project facts or known failures affect the next learning decision:

```markdown
## Artifact status
- Verified:
- Known failures:
```

Add `## Durable synthesis` only for a cross-cutting insight that will change future instruction. Mark it as a hypothesis until the learner demonstrates it in a fresh application.

## Update rules

- Rewrite and consolidate the snapshot in place. Do not append a session chronology.
- Keep exactly one active learner action. Split a compound action at the first observable checkpoint.
- Name both the verification target and the latest observed result. Use `not run` for a planned check rather than describing it as completed.
- Write observable evidence: quote the learner's explanation, summarize an attempt, or record a test result.
- Move older actions into evidence, review, or open questions.
- Record a misconception only when an attempt or explanation supports it; phrase it as a hypothesis if evidence is weak. When resolved, move the result into evidence and remove the stale gap.
- A capability moves to “Can do independently” after successful application to a new but related problem, not after recognition or agreement with an explanation.
- Record support for the current capability using the exact ladder in `SKILL.md`. Raise it only when the learner is blocked; lower it after successful independent progress.
- Retain only details that can change the next teaching decision. Add a separate source or notes file only when the learner needs material that will be reused.
