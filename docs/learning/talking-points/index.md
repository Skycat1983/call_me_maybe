# Waypoint Talking Points

These files prepare a voice-mode discussion for each learning waypoint.

## How to use them

Tell the agent:

> Read `docs/learning/talking-points/<waypoint-file>` and the linked waypoint.
> Use the voice-session guidance in that file. Help me explain the concepts in
> my own words before moving to implementation.

The talking-points file is the conversation guide. The corresponding waypoint
is the detailed historical record.

## Voice-session guidance

Unless a waypoint says otherwise, the agent should:

1. Read the talking-points file and its linked sources before beginning.
2. Start with a short recap of what was accomplished.
3. Ask one question at a time.
4. Let the learner explain first, then correct or extend the explanation.
5. Use concrete examples from this repository.
6. Distinguish confirmed facts, current assumptions, and unresolved questions.
7. Explain unfamiliar terms before relying on them.
8. Avoid implementing code unless the learner explicitly changes the session
   from discussion to implementation.
9. End with:
   - what the learner explained confidently;
   - what needs another pass;
   - unanswered questions;
   - the next recommended waypoint.

## Available discussions

| Waypoint | Talking points | Theme |
|---|---|---|
| 001 | [Repository and source files](001-repository-and-source-files.md) | Git, remotes, ignored files, extraction, and source artifacts |
| 002 | [Requirements and documentation](002-requirements-and-documentation.md) | Requirement extraction and human-centered documentation |
| 003 | [Tooling and storage](003-tooling-and-storage.md) | `uv`, dependencies, lockfiles, Makefile, environments, and caches |
| 004 | [Supplied data and LLM SDK](004-supplied-data-and-llm-sdk.md) | Data contracts, model loading, tokens, logits, imports, and constrained decoding |
| 005 | [Environment repair and cache placement](005-environment-and-cache-placement.md) | Installed environments, package caches, model caches, and reproducibility |
| 006 | [First SDK probe](006-first-sdk-probe.md) | Constructor failure, dependency versions, device mapping, and experiment choice |

## File convention

Each waypoint `NNN-YYYY-MM-DD-theme.md` gets a companion:

```text
docs/learning/talking-points/NNN-theme.md
```

The companion should link to the full waypoint and include:

- agent preparation;
- a short recap;
- key concepts;
- discussion prompts;
- understanding checks;
- likely misconceptions;
- unresolved questions;
- a successful-session outcome.
