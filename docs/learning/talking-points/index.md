# Talking Points Hub

This is the entry point for voice discussions and topic-centered learning.
Talking points now have two complementary paths: chronological waypoints and
living themes.

## Choose what you want to do

| Goal | Start here |
|---|---|
| Discuss recently completed work | [Waypoint discussions](waypoints/index.md) |
| Learn or revisit a topic | [Thematic discussions](themes/index.md) |
| Inspect primary command or experiment output | [Learning evidence](../evidence/index.md) |
| Understand current project direction | [Project status](../../project/status.md) |
| Review chronological progress | [Learning log](../index.md) |
| Maintain or reorganize talking points | [Maintenance guide](maintenance.md) |

## Current learning position

- Latest chronological record: [Waypoint 014 — CLI input shell](../waypoints/014-2026-11-17-cli-input-shell.md)
- Current progress discussion: [Talking points 014 — CLI input shell](waypoints/014-cli-input-shell.md)
- Current input theme: [Input validation and data models](themes/input-validation/index.md)
- Current CLI theme: [Command-line interface](themes/command-line-interface/index.md)
- Current tooling theme: [Python project tooling](themes/python-tooling/index.md)
- Current Git collaboration theme: [Branch reconciliation](themes/git-collaboration/index.md)
- Current code and SDK theme: [LLM SDK and `inspect_sdk`](themes/llm-sdk/index.md)
- Current deep technical guide: [Full `inspect_sdk` flow](themes/llm-sdk/runtime-flow/index.md)
- Current SDK terminal evidence: [2026-11-17 explicit-CPU run](../evidence/llm-sdk/2026-11-17-inspect-sdk-cpu.md)

The structural migration is complete. Chronological companions are under
`waypoints/`; living subject guides are under `themes/`. Waypoint 010 records
the original architecture work, and Waypoint 012 records the preparation-list
standard. Both are maintenance milestones without voice-discussion companions.

## Two documentation paths

### Chronological waypoint discussions

Use these when the question is:

> What did we just do, what evidence did we gather, and what should I now be
> able to explain?

Waypoint talking points are historical companions. They should remain mostly
stable after discussion and link to current thematic material for deeper
explanations.

### Living thematic discussions

Use these when the question is:

> Help me understand this subject, from an overview through theory and its
> application in this repository.

Thematic talking points are updated continuously as understanding, evidence,
and implementation develop. Mature themes can offer overview, concepts,
project-application, detailed-flow, and question routes.

## Standard voice-session guidance

Unless a guide says otherwise, the agent should:

1. Read the selected guide and open every repository file named in its
   `Files to have open` section.
2. Start with a short recap and state the intended depth.
3. Ask one question at a time.
4. Let the learner explain first, then correct or extend the explanation.
5. Use concrete examples from this repository.
6. Distinguish requirements, source facts, runtime observations,
   interpretations, assumptions, and unresolved questions.
7. Explain unfamiliar terms before relying on them.
8. Avoid implementation unless the learner explicitly changes the session's
   purpose.
9. End with confident areas, material needing another pass, unanswered
   questions, and the recommended next discussion.

## Suggested instruction for an agent

> Read `docs/learning/talking-points/index.md`, then follow the waypoint or
> theme route I name. Open every repository file in that guide's `Files to
> have open` section before beginning. Ask me one question at a time and help
> me explain the subject in my own words.

## Maintenance

- Repository instructions: [`AGENTS.md`](../../../AGENTS.md)
- Editorial rules: [maintenance guide](maintenance.md)
- Templates: [templates directory](templates/)
- Completed architecture record: [Waypoint 010](../waypoints/010-2026-11-13-talking-points-architecture.md)
