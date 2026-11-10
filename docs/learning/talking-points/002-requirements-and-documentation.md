# Talking Points 002: Requirements and Documentation

Companion waypoint:
[002 — Requirements and documentation](../waypoints/002-2026-11-06-requirements-and-documentation.md)

## Agent preparation

Read the companion waypoint and
[`docs/index.md`](../../index.md). Emphasize information architecture and the
difference between assignment requirements and implementation design.

## Short recap

The project PDF was condensed and preserved as an archive. Its actionable
content was split into focused requirement documents, with an index, status
page, task list, and evaluation checklist.

## Key concepts to discuss

1. Source material versus working documentation.
2. Stable knowledge, active state, and historical records.
3. Requirements describe **what**; design describes **how**.
4. A canonical home for each fact.
5. Linking instead of duplicating explanations.
6. Organizing documents around human questions.
7. The cost of both oversized documents and excessive fragmentation.

## Discussion prompts

- Why preserve the condensed subject after splitting it?
- Which document should answer “What must the output contain?”
- Which document should answer “What am I doing next?”
- Why should architecture not be written before understanding the SDK?
- What problems arise when the same rule is copied into several files?
- When is a new document justified?
- Why was the PDF's chapter order not used as the primary navigation?
- What makes the evaluation checklist different from the canonical
  requirements?

## Understanding checks

Ask the learner to place each item:

| Information | Expected home |
|---|---|
| Required JSON keys | Input/output contract |
| Current blocker | Project status or issues |
| Reason for choosing a state machine | Design decision |
| Original condensed subject | Archive |
| Submission verification | Evaluation checklist |
| Planned implementation task | Task list |

## Likely misconceptions

- A summary is not automatically the working source of truth.
- An evaluation checklist may repeat short verification statements, but it
  should link to the canonical requirement.
- More files do not always mean better organization.
- Design choices should not be presented as assignment mandates.
- Historical documents should not be silently rewritten to match later
  decisions.

## Successful session outcome

The learner can navigate from the documentation index to the right document
for a requirement, current task, design explanation, or historical source and
can explain why those categories are separate.
