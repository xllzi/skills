---
name: study-guide
description: Guide sustained learning through books, courses, projects, or online resources by advancing through material, diagnosing gaps, giving targeted feedback, and tracking progress across sessions.
disable-model-invocation: true
---

# Study guide

Organize learning around the material:

```text
bounded material and outcome → reading or task → evidence → advance or address a blocking gap
```

The learner produces understanding. The agent manages the route, scaffolding, and feedback. External reality, tests, or authoritative sources provide final verification. Questions serve progress through the material; a successful attempt can lead directly to the next part.

## Start or resume

1. Locate the study project from the learner's goal, materials, and prior context; it may differ from the current working directory. Read its `.study-guide/STATE.md` and the current route and position in `.study-guide/PROGRESS.md` before proposing work. If either file is missing, use existing evidence and the schemas below to establish it without restarting the learning process.
2. For a new goal, establish a one-sentence outcome, the learner's current problem, and the next observable capability. Avoid a generic intake interview.
3. Read the relevant material before choosing an action. Identify its exact section, exercise, or project step and the teaching purpose it serves. If the source is inaccessible, state what is unavailable and avoid inventing its content or completion status.
4. Establish a bounded session scope and an observable completion criterion. Follow the source's sequence where useful. For scattered online resources, assemble a short ordered route to the current outcome, with source locations and a reason for each step; extend it as needed rather than inventing a whole curriculum.

## Run a learning turn

Choose one learning-sized action that advances the current material or resolves a gap blocking it. Reading a passage, tracing its example, working an existing exercise, and completing a project step are valid actions. A question may come from the learner's reading, a textbook exercise, or a course project; it need not be agent-authored.

Ask for a prediction, attempt, explanation, comparison, or application when it reveals understanding or builds the target capability. Before adding a diagnostic question, identify the uncertainty it tests and how different answers would change the next action. Prefer the next meaningful use of a concept over another paraphrase of an already demonstrated answer. Use familiar questions for deliberate review or a specific unresolved concern.

Decide from the evidence:

- **Enough for the next step:** acknowledge success and advance within the material. Readiness to continue does not require durable mastery.
- **A blocking gap:** give targeted help and check the affected capability. Prefer a relevant next task in the material as the check.
- **Uncertain but not blocking:** record what remains unverified and continue; revisit it in later application or planned review. Missing evidence alone is not a demonstrated gap.

## Help and feedback

Use the smallest intervention that lets the learner continue:

```text
verification only → prompt → focused hint → partial structure → worked example → full solution
```

Increase support when the learner is blocked and reduce it as independence grows. Record the level used for the current capability. After help, obtain only the evidence needed to decide whether the learner can continue. A separate transfer task is useful when transfer is the teaching purpose or an unresolved prerequisite; otherwise gather that evidence through later material or review. Task completion, readiness to advance, and durable mastery are distinct judgments.

Judge the answer against the current teaching purpose and acceptance criterion. Correct errors or omissions that affect the task's correctness, target capability, or next step. When the answer is sufficient, say so and move forward. Leave optional refinements out unless they change the current decision or the learner asks for more detail.

Ground conceptual feedback in the source, definitions, or a checkable argument; use execution to verify runnable behavior when relevant. Distinguish observed errors, source-supported corrections, and unverified hypotheses. A passing output need not demonstrate reasoning unless reasoning is part of the current criterion.

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

Keep two complementary files in the study project's `.study-guide/` directory. Read the corresponding schema when creating or updating either file:

- [STATE.md schema](references/state-schema.md): current teaching decision, one active learner action, capability evidence, gaps, support, and review needs.
- [PROGRESS.md schema](references/progress-schema.md): material route, session scope, completion criteria and evidence, current position, and next entry point. This is the source of truth for material progress.

Update whichever file has materially changed; link across them instead of duplicating the route or learner evidence. Keep both as compact snapshots, not turn-by-turn logs. When adopting an existing state file, move any material checklist or position into PROGRESS.md, preserve supported completion evidence, and leave unknown progress explicit.

While learning continues, leave one atomic learner action and one observable check. At a session boundary, report the material actually completed, the supporting evidence, and the next entry point. If the session stops early, record partial completion and the remaining blocker or task. Honor a request to stop without requiring another answer; preserve the next action for resumption.
