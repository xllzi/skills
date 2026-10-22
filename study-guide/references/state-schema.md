# Cross-session state

Store durable learning state in `.study-guide/STATE.md` in the study project identified from the goal and materials. Create the directory only when a sustained learning goal exists.

Treat the file as a teaching-decision snapshot, not a session log. Material sequence, scope, completion, and position belong in [PROGRESS.md](progress-schema.md); link to its relevant entry rather than duplicating them here. Preserve the required headings below. Add an optional section only when it contains durable information that changes a future teaching decision.

When PLAN.md exists, its Goal and scope owns the overall learning goal. This file's Goal describes the capability currently being developed; link to the relevant stage rather than copying the overall plan. A plan remains optional.

Use this compact structure:

```markdown
# Study state

## Goal
- Outcome: one observable capability, not a topic name
- Why it matters:

## Current loop
- Material entry: link to the current unit in PROGRESS.md
- Problem:
- Next learner action: one observable action
- Mode: exploration | practice | verification | review | transfer
- Verification target:
- Latest result: not run | pass | fail — observation
- Advancement decision: continue | address blocking gap — evidence

## Evidence
- Can do independently:
- Can do with a hint:
- Not yet demonstrated: relevant uncertainty, not an assumed gap

## Misconceptions and gaps
- [ ] misconception or missing prerequisite — evidence — next check

## Scaffolding
- Current support reference: only a supplementary explanation or example needed for this action
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

Add `## Planning review` only when evidence or changed circumstances could change the overall route:

```markdown
## Planning review
- Affected stage: PLAN.md stage ID, or affected material if there is no plan
- Observed evidence: links to existing evidence, progress, or attributed learner reports
- Planning implication: why local adaptation may be insufficient
- Decision needed: the planning choice, including whether it blocks the current entry
```

This is a planning signal, not a second learner action or an automatic pause. Remove it after the decision is resolved, keeping any plan revision and rationale in PLAN.md. Retain only still-unresolved choices. Do not create an obligation merely because the learner skipped a question, requested advancement, or has not yet demonstrated a capability.

## Update rules

- Rewrite and consolidate the snapshot in place. Do not append a session chronology.
- Keep exactly one active learner action. Split a compound action at the first observable checkpoint.
- After a plan revision, check that the active action still serves the revised route. If entry reselection is required, preserve the earlier attempt and support evidence, then select one replacement action from the reconciled PROGRESS.md resume point before teaching resumes. A planning revision never upgrades an ability or completion claim by itself.
- Name both the verification target and the latest observed result. Use `not run` for a planned check rather than describing it as completed.
- Write observable evidence: quote the learner's explanation, summarize an attempt, or record a test result.
- Move older actions into evidence, review, or open questions.
- Record a misconception only when an attempt or explanation supports it; phrase it as a hypothesis if evidence is weak. When resolved, move the result into evidence and remove the stale gap.
- A capability moves to “Can do independently” after successful application to a new but related problem, not after recognition or agreement with an explanation.
- Readiness to advance is judged against the next material step. Keep supported task completion even when independent application or durable mastery remains unverified; schedule further evidence only where it changes a teaching decision.
- Record support for the current capability using the exact ladder in `SKILL.md`. Raise it only when the learner is blocked; lower it after successful independent progress.
- Retain only details that can change the next teaching decision. Add a separate source or notes file only when the learner needs material that will be reused.
