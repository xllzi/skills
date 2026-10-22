# Learning plan

Store the plan at `.study-guide/PLAN.md` in the actual study project. This shared directory lets existing study-guide projects adopt planning without migration. A one-off suitability assessment can remain in chat; do not create project state merely to answer it.

PLAN.md owns intended goals, resource choices, stage structure, and pacing. PROGRESS.md owns material completion and exact position. STATE.md owns capability evidence and the current teaching decision. Read [the handoff contract](study-guide-handoff.md) when connecting them.

## Structure

Use this compact snapshot for an adopted plan. Omit optional sections when they do not affect a decision. When a material choice remains unresolved, label the proposal and preserve the existing active route rather than silently replacing it.

```markdown
# Study plan

## Goal and scope
- Outcome: observable overall capability
- Why it matters:
- Included:
- Excluded or deferred:

## Constraints and assumptions
- Available effort: learner-provided constraint or explicitly unknown
- Deadline: hard deadline and reason, or none
- Relevant starting evidence: links or attributed learner reports
- Preferences affecting the route:
- Unverified assumptions: what could change the plan and how to check it

## Resource decisions
| Resource and source location | Edition or offering, if relevant | Role and when to use | Fit evidence and selection rationale |
| --- | --- | --- | --- |
| Main resource or sequence | Known version or unknown | Main line | Coverage, prerequisites, practice, and feedback |

## Stage plan
| Stage | Outcome | Material scope | Depends on | Completion criterion |
| --- | --- | --- | --- | --- |
| S1 | Observable capability | Module, chapter range, or project part | Prerequisite stage or capability | Observable use or result |

## Pacing
- Working rhythm or effort range:
- Estimates and basis: provisional until calibrated by actual study
- Date constraints and buffer: only when relevant

## Current focus and review
- Current stage:
- Learning entry: existing PROGRESS.md resume point, or an initial source location until learning starts
- Reassess when: concrete events or evidence that could change the route
- Open planning decisions: unresolved choices only

## Latest revision
- Date:
- Change and reason:
- Consequences: scope, resources, sequence, pacing, or required entry reselection
- Entry reconciliation: only for an invalidated entry; pending with affected stage/unit, or applied with a link to the new resume point
```

## Update rules

- Preserve stable stage IDs when reordering. Add new IDs for new stages. Do not renumber or reuse an ID referenced by progress; retain a compact identity and reason for removed or replaced stages when needed to interpret earlier evidence.
- Keep stage scope coarse and criteria meaningful. Exact sections, exercises, statuses, completion evidence, and stopping points belong in PROGRESS.md. Assess whether a stage meets its criterion from that file and STATE.md, without a parallel completion checklist in PLAN.md.
- Once a resume point exists, link to it instead of maintaining an independent next action. The overall goal lives here; STATE.md describes the capability currently being developed.
- Keep the current stage consistent with the established sequence. Advancing to the next already-planned stage is normal learning progression; changing the sequence, goal, or commitments is a planning decision.
- Distinguish plans and estimates from observations. Do not fill unknown time, prerequisite proficiency, or completion with plausible guesses. A trial result may support fit without demonstrating durable mastery.
- Keep one main line and only useful supplements. Preserve consequential selection reasons, not the full candidate search. Create a separate resource inventory only when its size or intended use justifies it.
- Keep near-term detail and coarse future stages. Do not force dates onto a self-paced route. If a calendar is requested, derive it from this plan; its views must not become a second independently maintained schedule.
- Latest revision is optional before any substantive revision. Replace it with the most recent meaningful change and its basis, not an accumulating session log. Keep still-relevant rationale in the affected decision itself.
- A revision changes expectations, not historical evidence. Preserve completed or skipped units and assistance levels. If it invalidates the current learning action, mark Entry reconciliation as pending with the affected stage/unit. Keep a pending reconciliation visible across further revisions until study-guide applies it as described in the handoff contract.
