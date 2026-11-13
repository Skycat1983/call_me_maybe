# Talking-Points Maintenance Guide

- Kind: Documentation maintenance
- Status: Living
- Last reviewed: 2026-11-13

This guide defines how chronological and thematic talking points are created,
updated, split, linked, and validated. Repository-wide agent behavior is
defined in the root `AGENTS.md`.

## Two complementary systems

### Waypoint talking points

Location:

```text
docs/learning/talking-points/waypoints/
```

Purpose:

- prepare a discussion of recently completed work;
- preserve the questions, evidence, decisions, and misconceptions relevant at
  that point in time;
- link the chronological waypoint to current thematic learning material.

Waypoint talking points are historical companions. After their discussion,
change them only to correct factual errors, repair links, or point to later
material.

### Thematic talking points

Location:

```text
docs/learning/talking-points/themes/
```

Purpose:

- explain a topic independently of when it was encountered;
- offer different depths and reading routes;
- combine theory with links to concrete repository application;
- evolve continuously as experiments and implementation add evidence.

Thematic documents are living material and should show a last-reviewed date.

## Choose the right destination

| Information | Destination |
|---|---|
| What happened during a particular round | Waypoint log |
| What to discuss about that round | Waypoint talking points |
| Current explanation of a reusable topic | Thematic talking points |
| Mandatory behavior | Requirements |
| Canonical API or technical facts | Reference documentation |
| Current unresolved question | Project question register |
| Reproducible observed defect | Known-issue register |
| Immediate objective and next actions | Project status |

## Progressive disclosure within a theme

A mature theme may contain:

```text
theme-name/
├── index.md
├── overview.md
├── concepts.md
├── project-application.md
├── questions.md
└── deep-dive-name/
    ├── index.md
    └── focused-stage.md
```

These filenames are options, not mandatory placeholders. Create only the
documents supported by meaningful content.

The theme index should offer routes such as:

- five-minute overview;
- theory or concepts;
- application in this repository;
- detailed execution or algorithm flow;
- questions and voice discussion.

## When to split a thematic file

Consider splitting when one or more conditions apply:

- it serves multiple independent learning goals;
- theory and project application obscure each other;
- readers need clearly different depth levels;
- navigation within the file becomes difficult;
- the file grows beyond roughly 300–500 lines;
- a section needs to be discussed or maintained independently.

Line count is a signal, not a rule. A coherent reference table can remain
long; a short file containing unrelated subjects should still be split.

## Standard metadata

Use a compact block near the top of a thematic document:

```markdown
- Kind: Thematic talking point
- Theme: Example theme
- Depth: Overview, applied, or detailed
- Status: Living
- Last reviewed: YYYY-MM-DD
- Prerequisites: None, or named documents
```

Waypoint companions instead identify their numbered waypoint and link it in
both directions. A maintenance-only waypoint can omit a companion when there
is no useful voice discussion to conduct.

## Standard related-learning section

End thematic documents with a contextual section resembling:

```markdown
## Related learning

- Theme home: theme index
- Prerequisite or previous depth
- Suggested next document
- Project application or theory counterpart
- Canonical requirement/reference
- Relevant chronological waypoints
- Relevant source files
```

Include only useful links. Do not add a repository-wide link dump to every
file.

## Voice-session design

A useful discussion guide should tell the agent to:

1. read the guide and its linked canonical sources;
2. recap the context briefly;
3. ask one question at a time;
4. let the learner explain first;
5. use concrete repository examples;
6. distinguish facts, observations, interpretations, and open questions;
7. avoid implementation unless the session explicitly changes purpose;
8. finish with confident areas, areas needing review, unanswered questions,
   and the recommended next discussion.

## Updating a theme after project work

After a relevant experiment or implementation step:

1. update facts and examples in the appropriate thematic document;
2. label new runtime evidence as observed rather than guaranteed;
3. add the new waypoint to related learning;
4. update the theme index's current status or recommended path;
5. move unresolved decisions into the project question register;
6. add a dated update note when the change is substantial;
7. split the file if the new material creates an independent learning route.

## Moving and restructuring files

- Inventory all inbound links before moving files.
- Use `git mv` so history remains easy to follow.
- Separate structural moves from major content rewriting where practical.
- Repair links in waypoint logs, references, indexes, experiment READMEs, and
  source comments.
- Do not leave compatibility stubs unless a real external link needs one.
- Confirm that no learner questions, observed results, or update history were
  lost during consolidation.

## Validation checklist

- [ ] All relative Markdown targets exist.
- [ ] Code fences are balanced.
- [ ] Headings and document titles are unique enough to navigate.
- [ ] Theme indexes expose overview, applied, and detailed routes where they
      exist.
- [ ] Waypoint and companion talking-points links work in both directions
      where a companion exists.
- [ ] The root talking-points index shows current locations.
- [ ] Metadata and last-reviewed dates are current.
- [ ] Related-learning sections are contextual and accurate.
- [ ] `git diff --check` passes.
- [ ] `git status` contains no unexplained files.
- [ ] Generated lockfiles were not manually edited.

## Templates

- [Waypoint talking points](templates/waypoint-talking-point.md)
- [Theme index](templates/theme-index.md)
- [Thematic topic](templates/thematic-topic.md)

## Related learning

- [Talking-points hub](index.md)
- [Waypoint discussions](waypoints/index.md)
- [Thematic discussions](themes/index.md)
- [Learning log](../index.md)
- [Project documentation](../../index.md)
