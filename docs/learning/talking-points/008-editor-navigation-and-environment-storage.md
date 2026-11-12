# Talking Points 008: Editor Navigation and Environment Storage

Companion waypoint:
[008 — Editor navigation and environment storage](../waypoints/008-2026-11-12-editor-navigation-and-environment-storage.md)

## Agent preparation

Read:

- the companion waypoint;
- `.vscode/settings.json`;
- `pyproject.toml` and the Makefile;
- [Python import resolution](../../reference/imports.md);
- the learner's question comments in `experiments/inspect_sdk.py`.

Explain concepts before suggesting commands. Do not remove learner question
comments during the voice discussion.

## Short recap

A uv-created repository `.venv` duplicated 1.1 GB of an environment that
already lived under `/tmp`, filling the small home filesystem. The duplicate
was removed and `.venv` became a link to the `/tmp` environment. Project and
VS Code settings now protect storage while preserving source navigation.

## Conversation order

1. Interpreter selection versus environment creation.
2. Physical storage versus the `.venv` discovery name.
3. What a symbolic link is and what happens when `/tmp` is cleared.
4. Makefile environment variables versus project-level uv settings.
5. How Pylance resolves imports and definitions.
6. How type annotations reveal methods such as `.tolist()`.
7. Pure Python definitions, type stubs, and compiled methods.

## Key evidence

| Observation | Meaning |
|---|---|
| Home was 99% full with only 60 MB free | Editor and shell operations were at risk of failing |
| Repository `.venv` used 1.1 GB | A second environment was consuming the constrained filesystem |
| `.venv/pyvenv.cfg` named uv 0.12.5 | uv created it; it was not a Pylance index |
| `/tmp/call-me-maybe-venv` still used 5.5 GB | The intended complete environment remained available |
| No process used the local `.venv` | The incomplete duplicate could be safely removed |
| Home returned to 77% usage | Removing the duplicate reclaimed the expected capacity |
| `uv cache dir` reports `/tmp/...` | Bare uv commands now honor the project cache setting |

## Discussion prompts

- Does selecting an interpreter install packages? What does it actually tell
  VS Code?
- Why can a Makefile variable protect `make install` but not necessarily a uv
  command started elsewhere?
- What evidence shows that uv created the accidental `.venv`?
- What can we conclude about cause, and what can we not prove?
- Why is a symbolic link useful here?
- What happens to that link if `/tmp` is cleared?
- Why does the ignore rule use `.venv` rather than `.venv/`?
- How does `python.analysis.extraPaths` change where Pylance looks?
- How does the return annotation `-> torch.Tensor` help with `.tolist()`?
- When might Ctrl+click open a stub rather than implementation source?
- Why is `tuple(encoded.shape)` optional?

## Understanding checks

Ask the learner to explain this chain:

```text
Small_LLM_Model.encode annotation
    -> Pylance infers torch.Tensor
    -> hover/completion reveals tensor members
    -> .tolist() converts values to normal Python data
```

Ask the learner to distinguish these paths:

```text
.venv                              conventional local discovery name
/tmp/call-me-maybe-venv            physical installed environment
/tmp/call-me-maybe-uv-cache        downloadable package cache
/tmp/call-me-maybe-huggingface     model and tokenizer cache
```

## Likely misconceptions

- Selecting an interpreter is not the same operation as creating one.
- The timing does not prove that the selection click itself invoked uv.
- Pylance does not need a second copy of every installed package.
- A symbolic link consumes almost no space but its target still does.
- Clearing `/tmp` removes the target data, not the project configuration or
  lockfile needed to recreate it.
- `.tolist()` is discoverable API knowledge, not something the learner must
  guess.
- Ctrl+click cannot always expose compiled C/C++ implementation as Python.
- `tuple(encoded.shape)` changes display form, not tensor shape.

## Practical VS Code check

After reloading the window:

1. Confirm the status bar shows the `.venv` or `/tmp` Python interpreter.
2. Ctrl+click `Small_LLM_Model` and note the opened path.
3. Go back, then Ctrl+click `ArgumentParser` and note that path.
4. Hover over `encoded` and identify its inferred type.
5. Type `encoded.` and locate `tolist` in completion suggestions.
6. Use F12 if Ctrl+click is captured by a different editor action.

## Successful session outcome

The learner can explain why the filesystem filled, why the duplicate was safe
to remove, how the symlink prevents a repeat, and how interpreter selection,
type annotations, Pylance, and Go to Definition work together without another
installation.
