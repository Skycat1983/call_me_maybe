# Waypoint 010: Talking-Points Architecture

- Date: 2026-11-13
- Stage: Learning-system organization
- Status: Complete

Voice discussion: Not required. This is a maintenance record rather than a
substantive project theme.

## Purpose

Plan and establish a documentation system that separates chronological
discussion of recent work from living, topic-centered learning material.

## Starting problem

All talking points shared one directory. Files 001–009 were chronological
waypoint companions, while the SDK agent briefing and 1,091-line full-flow
guide were already thematic and continually maintained.

That mixture made it unclear:

- whether a document represented history or current understanding;
- where future agents should add new explanations;
- how a learner should choose overview, theory, application, or deep detail;
- when a long thematic guide should be divided;
- how related materials should link to one another.

## Decision

Talking points will have two complementary paths:

```text
talking-points/
├── waypoints/    chronological discussion companions
└── themes/       living topic-centered learning guides
```

Waypoint talking points remain mostly stable after their discussion. Thematic
talking points are updated as knowledge, experiments, and application code
develop.

## Progressive thematic depth

A mature theme may offer:

- a surface-level overview;
- concepts and theory;
- application in this repository;
- detailed runtime or algorithm flows;
- questions and voice-session prompts.

These are optional reading routes rather than mandatory empty files. Material
should be split when it serves independent learning goals or becomes difficult
to navigate, with 300–500 lines used as a warning signal rather than a rigid
limit.

## Navigation decision

The root talking-points index now routes by learner goal. Waypoint and theme
indexes provide their own maps. Thematic documents will use metadata and a
contextual `Related learning` section pointing to their theme home,
prerequisites, next depth, project application or theory counterpart,
canonical references, relevant waypoints, and source files.

## Agent instructions

A root `AGENTS.md` now instructs future agents to:

- work learning-first;
- read status, indexes, relevant waypoints, themes, requirements, and
  references before meaningful changes;
- preserve learner `# ?` questions and answer them clearly;
- distinguish historical and living documentation;
- update the correct registers and indexes;
- avoid manual lockfile edits;
- validate links, fences, diffs, and working-tree state;
- avoid committing or pushing without a request.

Detailed editorial procedures live in the talking-points maintenance guide so
the automatically discovered root instruction file can remain focused.

## Phase 1 changes

Created:

- root `AGENTS.md`;
- a redesigned talking-points hub;
- waypoint and thematic indexes;
- a maintenance guide;
- waypoint, theme-index, and thematic-topic templates;
- this waypoint and its companion in the new chronological location.

No existing talking-points content was moved or split in Phase 1. This avoids
breaking current links before the navigation rules and migration map exist.

## Original migration plan

1. Phase 2: move waypoint companions 001–009 with `git mv` and repair links.
2. Phase 3: create the Python-tooling and LLM-SDK theme directories.
3. Phase 4: split and consolidate the two large SDK thematic guides.
4. Phase 5: add contextual navigation throughout thematic material.
5. Phase 6: validate all links, fences, titles, metadata, and indexes.
6. Phase 7: commit structural moves separately from thematic consolidation.

## Completion update

The learner chose to complete the maintenance work without a voice discussion
about documentation architecture. The final structure now:

- stores companions 001–009 under `talking-points/waypoints/`;
- stores living SDK guides under `talking-points/themes/llm-sdk/`;
- provides a practical Python-tooling thematic index;
- provides an LLM-SDK thematic index with routes into source, results, runtime
  stages, and discussion questions;
- removes the unnecessary Waypoint 010 discussion companion;
- routes current discussions toward project configuration, code, progress,
  and technical themes.

The two long SDK guides were split at meaningful learning boundaries. The
probe material now separates overview, source walkthrough, runtime evidence,
and question-led discussion. The detailed flow now separates command entry,
model construction, encoding/decoding, tokenizer files, logits/ranking, and
the variable-ledger discussion.

The workspace exposes `.git/index` as read-only, so `git mv` could not record
the moves directly. Equivalent filesystem moves were used without changing
content; Git can detect the renames when the files are later staged.

## Validation results

- All 293 relative Markdown links resolved across the 56 Markdown files
  checked.
- All 26 relative heading-anchor links reached real headings.
- Code fences were balanced across all Markdown files checked.
- Every LLM-SDK thematic document had exactly one top-level heading.
- The initial mechanical split preserved all 1,839 source lines before
  navigation metadata and links were added.
- `git diff --check` passed.
- The working tree was reviewed with `git status`; the earlier uncommitted
  Waypoint 009, configuration, SDK-probe, and inline explanation work remains
  present alongside this phase.

## Next step

Use the Python-tooling or LLM-SDK theme for a substantive voice discussion,
then continue the project's technical learning sequence.
