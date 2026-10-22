# Planning and learning handoff

Use the study project's `.study-guide/` files to communicate across skills or chats. Neither skill requires a separate agent, a new conversation, or the entire prior transcript. Existing learning can continue without PLAN.md, and planning can produce a useful route without study-guide being installed.

If study-planing is unavailable, study-guide can continue local learning while recording evidence and surfacing unresolved planning choices. Do not invent a replacement route merely to bypass a missing skill.

## Information ownership

| Information | Home | Responsibility |
| --- | --- | --- |
| Overall goal, resource decisions, stage definitions, cross-stage pacing | PLAN.md | study-planing maintains planning decisions |
| Current stage | PLAN.md | study-guide may advance this pointer through the agreed route |
| Entry reconciliation after a route change | PLAN.md Latest revision | study-planing marks it pending; study-guide marks it applied after reconciling the entry |
| Exact material route, completion facts, session scope, resume point | PROGRESS.md | study-guide maintains actual material progress |
| Current capability, learner action, evidence, gaps, support | STATE.md | study-guide maintains teaching decisions |
| Request to reconsider the route | Optional Planning review in STATE.md | study-guide raises it; study-planing resolves the planning question |

The local schemas for PROGRESS.md and STATE.md live with study-guide; do not reproduce them here. Find study-guide in the installed skills when needed; in this repository its schemas are [material progress](../../study-guide/references/progress-schema.md) and [study state](../../study-guide/references/state-schema.md). If unavailable, leave PLAN.md's learning entry usable without creating guessed companion state.

Apart from advancing the current-stage pointer through the agreed route and marking entry reconciliation applied, study-guide leaves PLAN.md's decisions to the planning role. Revising a plan changes expectations, not recorded completion or capability evidence.

## From planning to learning

1. study-planing leaves a current stage, relevant source scope, completion criterion, and review conditions. On an existing project, it links to the real resume point rather than resetting the learner to the start.
2. study-guide reads the relevant plan sections at startup and after material planning changes. Expand only the near-term stage into material units. When a plan exists, associate units with stable stage IDs using the optional Stage column in PROGRESS.md; do not force a mapping for unrelated exploratory work or reconstruct missing history.
3. Set a bounded session scope from the stage and actual stopping point. Keep exactly one active learner action and one observable check in STATE.md. Its Goal is the current capability; the overall goal stays in PLAN.md.
4. Update material completion and capability evidence where they belong. At a planned stage boundary, check the criterion against that evidence and advance PLAN.md's current-stage pointer when the established route calls for it. Do not turn routine progression into a mandatory planning session; surface only review conditions that could change the next decision.

A trial uses the same learning loop, with a bounded material entry and a stated fit question. It does not require a whole-course plan. Preserve the trial's evidence if a longer route is later adopted.

## Local adaptation and planning review

study-guide may narrow or slow down a session, change examples or hints, add a local supplement, or reorder local exercises while preserving stage outcomes and commitments. A request such as "slow down" or "let's do less today" is a local teaching adjustment, not by itself a planning review. It can continue meaningful work while a nonblocking planning question remains open.

Planning owns cross-stage pacing: allocating effort among stages, changing their time windows or deadlines, or revising the overall learning schedule. If a local adjustment has a sustained effect on those commitments, surface that effect for planning rather than treating every session-level change as a route change.

For repeated prerequisite obstruction, sustained effort mismatch, unavailable core material, or changed goals, record an optional `Planning review` in STATE.md. Follow that file's schema: affected stage, observed evidence, planning implication, and decision needed. Link to existing evidence; do not copy it or add another learner action. One difficult attempt, a skipped question, a request to move on, or an unknown capability alone is not a reason to create a review obligation.

Replacing the main course, changing the overall goal, substantially reducing scope, or adding a substantial stage belongs to study-planing. If the learner already directed the change, apply it. Otherwise present the proposed change and its consequences before replacing the active route. A review signal does not automatically invoke another skill or suspend learning.

## Return after a revision

Read the planning review and its supporting progress before changing PLAN.md. Resolve only the affected decision. Preserve observed completion, skips, uncertainty, and support levels in their existing files.

If the revision makes the current action unsuitable, mark Entry reconciliation as `pending` with the affected stage/unit in PLAN.md's Latest revision. Before teaching resumes, study-guide must reconcile the plan with PROGRESS.md and STATE.md: preserve the previous attempt as evidence or partial progress, replace the resume point, and set one valid active action. Then mark Entry reconciliation as `applied` with a link to the new resume point; retain the revision rationale and do not reselect again on every resumption. The planner must not present the old action as still executable; if learning continues in the same chat, perform this reconciliation immediately in the study-guide role.

After applying the decision, remove the resolved Planning review from STATE.md or retain only the still-unresolved choice. The rationale belongs in PLAN.md, not a duplicated review history. Retaining the existing route is also a valid resolution when supported by the evidence.
