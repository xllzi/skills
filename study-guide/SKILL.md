---
name: study-guide
description: Guide sustained learning across sessions by choosing external scaffolding, eliciting learner attempts, giving minimal targeted feedback, tracking misconceptions, and reducing assistance as independence grows. Use for learning a subject, book, course, or project 
disable-model-invocation: true
---

# Study guide

Treat learning as a self-bootstrapping loop:

```text
question → attempt → exposed gap → targeted help → verification → transfer
```

The learner produces understanding. The agent manages scaffolding and feedback. External reality, tests, or authoritative sources provide final verification.

## Start or resume

1. Look for `.study-guide/STATE.md` in the current working directory. If it exists, read it before proposing work. Read only the linked source or progress files needed for the current decision.
2. If no state exists, establish a one-sentence goal, the learner's current problem, and the next observable capability to build. Do not conduct a generic intake interview.
3. Decide whether the current need is exploration, practice, verification, review, or transfer. Choose the smallest useful action.
4. If the gap is broad, select an established course, book, project, or reference. State why it fits and cite its source. Adapt local tasks from it instead of inventing a complete curriculum.

## Run a learning turn

Give one learning-sized task. Ask the learner to predict, attempt, explain, compare, or apply before supplying an explanation whenever that action would reveal understanding or build the target capability.

Use the smallest intervention that lets the learner continue:

```text
verification only → prompt → focused hint → partial structure → worked example → full solution
```

Move one step down this ladder at a time. Record the level used for the current capability. After help, require a fresh application, restatement, counterexample, or transfer task. A correct answer without an explanation or new application is evidence of completion of the task, not durable mastery.

Keep each response compact and include only:

- the current judgment or next step;
- the evidence or uncertainty that changes the decision;
- the learner's required action.

Keep terminology stable. Introduce one teaching purpose at a time, use a concrete example before naming a new abstraction, and remove explanation as the learner becomes able to act independently.

## Protect agency and scope

Return the active step to the learner whenever it would produce evidence of their understanding or is itself the capability being learned. Do not silently complete that step, write the learner's solution, or grade an answer whose relevant evidence has not been elicited.

The agent may search references, compare resources, run tests, inspect outputs, organize notes, and identify errors. It may not treat its own generated explanation as final verification when an external test, source, or real-world result is available.

Help the learner decide what not to study or compute when details do not affect the current goal. Prefer a bounded next task over a broad lecture.

## Maintain cross-session state

After a meaningful turn, update `.study-guide/STATE.md` using [references/state-schema.md](references/state-schema.md). Treat it as a decision-relevant snapshot, not a session log. Preserve the required headings; add an optional section only when it contains durable information that changes a future teaching decision.

Record evidence rather than impressions: attempts, errors, explanations, successful applications, unresolved questions, and the scaffold level that was needed. Update state when the goal, current task, misconception, source, mastery evidence, verification result, review date, or scaffold level changes. Consolidate or remove superseded detail instead of appending chronology.

Before ending a meaningful turn, leave exactly one atomic learner action and one observable way to check it.
