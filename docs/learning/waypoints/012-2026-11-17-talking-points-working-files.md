# Waypoint 012: Talking-Points Working Files

- Date: 2026-11-17
- Stage: Documentation maintenance
- Status: Complete
- Voice discussion: None; this is a maintenance-only waypoint

## Purpose

Make every voice-discussion guide state exactly which repository files the
learner and agent should have open while discussing that point. Preserve the
same convention when future waypoint and thematic guides are created or
expanded.

## Problem addressed

Existing guides were inconsistent. Some waypoint companions named files in
their preparation prose, while thematic guides often left source links until
the final navigation section. A voice agent could therefore understand the
topic but still have to infer which code, configuration, evidence, or
requirement files the learner should be viewing.

## Decision

Every actual waypoint or thematic discussion guide now has a near-top section
with the exact heading:

```markdown
## Files to have open
```

Each entry links to a specific repository file and briefly explains what to
inspect there. This section is the conversation's focused working set. The
end-of-file `Related learning` section remains broader onward navigation and
does not replace it.

General navigation indexes direct the agent to the selected guide's working
set rather than repeating all of its links.

## Progress made

- Added the section to all 10 existing waypoint discussion companions.
- Added the section to all 15 existing thematic indexes and focused SDK
  guides.
- Separated file preparation from discussion-conduct instructions in waypoint
  companions.
- Added the rule to `AGENTS.md` and the talking-points maintenance guide.
- Updated all three talking-points templates so new guides start with the
  required section.
- Updated hub and index instructions so voice agents open the listed files
  before beginning.
- Added explicit validation checks for the section, its links, and its stated
  purposes.

## Questions and answers

### Why use one exact heading?

A stable heading is easy for a human or agent to find and easy to validate
across the documentation tree.

### Why list a reason beside every file?

A filename alone does not say whether the learner should inspect a class, a
test case, a command, a requirement, or recorded output. The short reason
makes the file useful during a live conversation.

### Why not rely on `Related learning`?

Related-learning links answer “where could I go next?” The working-file list
answers “what should be on screen for this discussion?” Combining those roles
would either overload preparation or omit useful navigation.

### How will future guides preserve this behavior?

Future agents are instructed by `AGENTS.md`; maintainers have a canonical
rule and checklist; and each reusable template contains the section. When a
guide's scope or file locations change, its working-file list must change too.

## Validation evidence

- All 25 existing discussion guides contain the expected heading.
- Relative Markdown targets were checked after the edits.
- Markdown code fences and whitespace were checked.
- No source code, runtime configuration, dependency declaration, or generated
  lockfile changed.

## Documents created or updated

- [`AGENTS.md`](../../../AGENTS.md)
- [Talking-points maintenance guide](../talking-points/maintenance.md)
- [Talking-points templates](../talking-points/templates/)
- [Waypoint discussion guides](../talking-points/waypoints/)
- [Thematic discussion guides](../talking-points/themes/)
- [Talking-points hub](../talking-points/index.md)
- [Project status](../../project/status.md)

## Next step

Return to the application objective: discuss the Pydantic input models as
needed, then implement and test the focused JSON-loading boundary.
