# Project Instructions for Agents

This repository is both a software project and a learning record. Help the
learner understand decisions and evidence before moving to implementation.

## Read before working

Before making a meaningful change, read:

1. `docs/project/status.md`;
2. `docs/learning/index.md`;
3. `docs/learning/talking-points/index.md`;
4. the latest relevant waypoint;
5. the relevant thematic talking-points index, requirement, or reference.

Inspect the working tree before editing. Existing changes may belong to the
learner or another unfinished step; preserve them and do not overwrite them.

## Learning-first collaboration

- Explain unfamiliar concepts before relying on them.
- Before an experiment, state its question, controlled change, expected
  evidence, and how success or failure will be interpreted.
- Distinguish requirements, source-code facts, runtime observations,
  interpretations, assumptions, and unresolved questions.
- Let the learner explain concepts in their own words during discussion
  sessions before correcting or extending the explanation.
- Do not turn a discussion request into implementation without authorization.

The learner writes question comments beginning with `# ?` or `#?`. Preserve
their wording. Add a concise `# Answer:` immediately below when an inline
answer is appropriate. Use real module, class, or function docstrings for API
documentation; do not add unused triple-quoted string expressions merely to
imitate docstrings.

## Documentation roles

- `docs/requirements/`: what the project must satisfy.
- `docs/reference/`: canonical reusable technical facts.
- `docs/project/`: current status, tasks, open questions, and known issues.
- `docs/learning/waypoints/`: chronological records of meaningful progress.
- `docs/learning/talking-points/waypoints/`: discussion guides for individual
  chronological waypoints.
- `docs/learning/talking-points/themes/`: living, topic-centered learning
  guides that are updated as understanding grows.
- `docs/archive/`: retained source-derived or superseded material.

Waypoint records preserve history. Do not rewrite an earlier conclusion merely
because understanding later changed; add a correction or link from a newer
waypoint. Thematic talking points describe current understanding and should be
updated in place.

Talking points are a conversational learning layer, not a substitute for
requirements or canonical references. Link to the canonical source instead of
duplicating long explanations unnecessarily.

Detailed editorial rules and templates are in
`docs/learning/talking-points/maintenance.md`.

## After meaningful work

Decide whether the work requires:

- a new chronological waypoint and companion talking-points file;
- an update to one or more living thematic documents;
- a reference correction;
- an open-question or known-issue update;
- a project status or task update;
- index and related-learning link updates.

Create a waypoint for a new objective, meaningful experiment, decision,
technical theme, implementation milestone, or substantial group of answered
questions. Do not create one for a spelling correction or trivial command.

## Thematic talking-point rules

- Each theme has an `index.md` that offers reading routes by goal and depth.
- Prefer progressive disclosure: overview, concepts/theory, project
  application, and deep dives where the material warrants them.
- Do not create empty files merely to satisfy a uniform directory shape.
- Consider splitting a file when it serves independent learning goals, mixes
  theory and application confusingly, or grows beyond roughly 300–500 lines.
- Include metadata, prerequisites, related material, canonical references,
  source links, relevant waypoints, and a last-reviewed date.
- Add or update navigation when files move or themes grow.

## Source and generated files

- Treat `pyproject.toml` as human-authored dependency intent.
- Treat `uv.lock` files as generated resolutions; do not hand-edit them.
- The supplied SDK may be explained internally, but project application code
  must obey the public-interface restriction.
- Large reproducible environments and caches belong under the configured
  `/tmp` paths, not the small home filesystem.
- Keep the supplied PDF and generated output out of Git as configured.

## Validation

Validate in proportion to the change. For documentation restructuring:

- preserve moves with `git mv` when appropriate;
- check relative Markdown links;
- check balanced code fences;
- run `git diff --check`;
- inspect `git status` and the complete diff;
- confirm indexes, breadcrumbs, and related-learning sections agree.

For Python or configuration changes, also run the relevant syntax, lint,
lockfile, and dry-run checks documented by the project.

Do not commit or push unless the learner requests it.
