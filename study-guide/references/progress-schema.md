# Material progress

Store the material route and completion evidence in `.study-guide/PROGRESS.md`, beside STATE.md in the study project. Read its current scope and position when resuming; consult older entries only when they affect the next decision.

Use this compact structure, adapting the unit size to the source:

```markdown
# Study progress

## Session scope

- Target outcome:
- Bounded material: unit IDs from the route below
- Completion criterion: observable use or understanding of this material

## Material route

| Unit | Source and exact location | Purpose and completion criterion | Status | Completion evidence |
| --- | --- | --- | --- | --- |
| U1 | URL or path plus section, exercise, or project step | What this unit enables and what counts as done | in progress | Observed result or link to evidence; unknown if unavailable |

## Resume point

- Current position: unit ID and exact stopping point
- Next entry: next passage, exercise, or project step
- Remaining work or blocker:
```

## Update rules

- When PLAN.md exists, add an optional `Stage` column to Material route and associate relevant units with its stable stage IDs (for example, S1). Leave unrelated exploratory units explicitly unassigned; preserve unmapped older entries rather than guessing their history. Keep exact source locations here and coarse stage scope in PLAN.md. Without a plan, keep the existing structure.
- Keep a short ordered route to the current outcome. Use the material's structure when available; for scattered resources, make the relationship between successive units clear through their purposes. Extend the route when the next learning need becomes concrete.
- Use `not started`, `in progress`, `completed`, or `skipped`. State the reason for a skipped unit; it is not completed. Preserve completed units compactly so resumption does not restart known material.
- Define completion against the unit's teaching purpose. Reading a passage is enough when orientation is the purpose; applying a method requires evidence of application. Merely opening a source or receiving an explanation does not establish absorption.
- Mark completion only from observed evidence or explicitly attributed learner reports. Distinguish assisted completion from independent performance by linking to the evidence in STATE.md or the learner's artifact. Material completion is not a claim of durable mastery.
- Keep source references and positions here. Keep misconceptions, support levels, independent capability claims, and review needs in STATE.md. Its active learner action implements this file's resume point; avoid maintaining a second competing action list.
- Update at material checkpoints, scope changes, and session boundaries. Record partial completion honestly when time runs out or a blocker remains; keep unresolved work visible before replacing the session scope.
- When migrating an existing study record, preserve established progress and label unknown history as unknown. Do not reconstruct completion from a list of topics mentioned in conversation.
- When a plan is adopted or revised, preserve unit IDs, completion evidence, skips, and partial attempts. Reconcile any invalidated resume point with the revised stage before learning resumes, and update STATE.md's active action to match. Changes to expected material do not rewrite historical completion. Judge planned stage completion from these facts and relevant capability evidence; do not maintain a second completion checklist in PLAN.md.
