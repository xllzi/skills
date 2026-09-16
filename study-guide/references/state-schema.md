# Cross-session state

Store durable learning state in `.study-guide/STATE.md` in the current project. Create the directory only when a sustained learning goal exists.

Use this compact structure:

```markdown
# Study state

## Goal
- Outcome: one observable capability, not a topic name
- Why it matters:

## Current loop
- Problem:
- Next learner action:
- Mode: exploration | practice | verification | review | transfer
- External reality or source used for verification:

## Evidence
- Can do independently:
- Can do with a hint:
- Not yet demonstrated:

## Misconceptions and gaps
- [ ] misconception or missing prerequisite — evidence — next check

## Scaffolding
- Current source:
- Current support level: full example | worked structure | focused hint | verification only
- Removal condition:

## Review and transfer
- Review when:
- Transfer task:
- Open questions:
```

## Update rules

- Write observable evidence: quote the learner's explanation, summarize an attempt, or record a test result.
- Keep one active next action. Move older actions into evidence, review, or open questions.
- Record a misconception only when an attempt or explanation supports it; phrase it as a hypothesis if evidence is weak.
- A capability moves to “Can do independently” after successful application to a new but related problem, not after recognition or agreement with an explanation.
- Raise the support level only when the learner is blocked; lower it after successful independent progress.
- Prefer updating this file over creating session transcripts. Add a separate source or notes file only when the learner needs material that will be reused.
