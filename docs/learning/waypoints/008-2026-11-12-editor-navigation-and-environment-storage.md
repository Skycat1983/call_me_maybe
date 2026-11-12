# Waypoint 008: Editor Navigation and Environment Storage

- Date: 2026-11-12
- Stage: Development environment and source navigation
- Status: Complete

Voice discussion:
[Talking points 008](../talking-points/008-editor-navigation-and-environment-storage.md)

## Purpose

Make VS Code definition navigation work without duplicating the large Python
environment onto the small home/profile filesystem.

## Starting problem

VS Code was told to use:

```text
/tmp/call-me-maybe-venv/bin/python
```

Soon afterward, the home filesystem reached 99% usage. A new repository-local
`.venv` occupied 1.1 GB while the intended 5.5 GB environment still existed
under `/tmp`.

The goal was not merely to reclaim space. The editor still needed enough
information to navigate from symbols such as `Small_LLM_Model`,
`ArgumentParser`, and tensor methods to their definitions or documentation.

## Evidence gathered

Filesystem measurements showed:

```text
home filesystem: 4.7 GB total, 60 MB free, 99% used
/tmp filesystem: 327 GB total, 225 GB free, 28% used
repository .venv: 1.1 GB
/tmp project environment: 5.5 GB
```

The local `.venv/pyvenv.cfg` contained:

```text
uv = 0.12.5
```

Its files all had the current creation time. It was therefore a newly created,
incomplete uv environment, not a Pylance index or a required copy of the
selected `/tmp` interpreter.

No process was using the local environment. It was ignored by Git and fully
reproducible from `pyproject.toml` and `uv.lock`.

The intended interpreter successfully resolved:

```text
ArgumentParser -> Python standard-library argparse.py
Small_LLM_Model -> installed llm_sdk package under /tmp
```

## Important causal distinction

Selecting an interpreter tells VS Code which Python installation its language
features, run commands, and debugger should use. Selection should not require
copying every installed package into the repository.

The evidence proves that uv created the second `.venv`; it does not prove that
the act of clicking **Python: Select Interpreter** directly created it. A uv
operation launched outside the Makefile—or an environment-management action
in the editor—would not inherit the Makefile's exported
`UV_PROJECT_ENVIRONMENT` value. Without that override, uv's normal project
location is `.venv`.

## Repair

The incomplete repository `.venv` was removed, reclaiming approximately
1.1 GB. Home usage fell from 99% to 77%, leaving approximately 1.1 GB free.

A lightweight link now occupies the conventional project path:

```text
.venv -> /tmp/call-me-maybe-venv
```

This provides both behaviors:

- editors and tools that automatically look for `.venv` can find it;
- the actual packages remain on the large `/tmp` filesystem.

If `/tmp` is cleared, the link may temporarily point to a missing target.
Running `make install` recreates the target from the lockfile, after which the
same link works again.

The `.gitignore` rule changed from `.venv/` to `.venv`. A trailing slash only
matched a real directory; the new form also ignores the machine-specific
symbolic link.

## Project safeguards

### uv settings

The root `pyproject.toml` now contains:

```toml
[tool.uv]
cache-dir = "/tmp/call-me-maybe-uv-cache"
link-mode = "copy"
```

This protects bare uv commands, not only commands run through Make. A
validation command confirmed that `uv cache dir` now reports the `/tmp` path.

The environment path itself remains represented by the `.venv` link because
uv exposes `UV_PROJECT_ENVIRONMENT` as an environment-variable override rather
than a normal project setting.

### VS Code settings

Workspace settings now specify:

- `${workspaceFolder}/.venv/bin/python` as the default interpreter;
- `${workspaceFolder}/llm_sdk` as an additional Pylance source path;
- a project environment file containing the `/tmp` paths;
- the same paths for new integrated terminals.

The extra source path is important for learning. The interpreter contains an
installed SDK copy, but this repository also contains its readable source.
Pylance can now resolve `llm_sdk` directly to the local source being annotated.

## How Ctrl+click works

Ctrl+click and F12 are editor operations usually called **Go to Definition**.
For Python, Pylance combines several information sources:

1. the selected interpreter;
2. the interpreter's standard library and installed packages;
3. the open workspace's Python files;
4. configured analysis paths;
5. type annotations and type stubs.

No additional package installation is required when those locations already
contain the source or type information.

Expected destinations in this project include:

- `Small_LLM_Model`: local `llm_sdk/llm_sdk/__init__.py` through the configured
  analysis path;
- `ArgumentParser`: the selected interpreter's standard-library `argparse.py`;
- some compiled-library methods: a Python type stub or attached documentation
  rather than their low-level compiled implementation.

## Questions and answers

### How am I supposed to know that `.tolist()` exists?

You are not expected to memorize every method supplied by every library.

The SDK declares:

```python
def encode(self, text: str) -> torch.Tensor:
```

That return annotation lets Pylance infer that `encoded` is a
`torch.Tensor`. From there, the method is discoverable by:

- hovering over `encoded` to inspect its inferred type;
- typing `encoded.` and reading the completion list;
- Ctrl+clicking or pressing F12;
- using `help(torch.Tensor.tolist)` in Python;
- searching installed source or consulting PyTorch documentation.

Runtime inspection confirmed that `torch.Tensor.tolist` returns tensor values
as a nested Python list, or a Python number for a scalar. Because `encoded[0]`
is one-dimensional, it produces the flat `list[int]` required by the SDK's
logits method.

### Why convert `encoded.shape` to a tuple?

It is only for clearer diagnostic output:

```text
encoded.shape        -> torch.Size([1, 11])
tuple(encoded.shape) -> (1, 11)
```

Both describe the same dimensions. The model does not require the conversion.

### Why keep a `.venv` name if packages live elsewhere?

`.venv` is a strong convention understood automatically by uv, VS Code, and
other Python tools. A symbolic link preserves that discoverability while its
target controls where the storage is physically consumed.

### Will Ctrl+click always show ordinary Python source?

No. Pure Python classes commonly open their `.py` definitions. Standard
library symbols can open the selected Python installation's source. Methods
implemented in compiled extensions may lead to a `.pyi` type stub,
documentation declaration, or a Python wrapper instead of C/C++ internals.

## Validation

- The workspace settings file parses as valid JSON.
- `uv cache dir` reports `/tmp/call-me-maybe-uv-cache`.
- `uv run --no-sync` uses `.venv/bin/python`, which resolves through the link.
- `argparse` and `llm_sdk` import successfully.
- Git ignores the `.venv` link.
- Home usage is 77% rather than 99%.
- `/tmp` still has approximately 225 GB free.

## Decisions

- Keep all large packages, uv cache data, and model files under `/tmp`.
- Keep `.venv` only as an ignored link for tool discovery.
- Configure uv at project level as well as through the Makefile.
- Configure VS Code to prefer local SDK source for definition navigation.
- Treat source-navigation tools as a way to discover APIs, not as something a
  learner is expected to replace with memorization.

## Next step

Reload the VS Code window so all workspace settings are applied. Then test:

1. Ctrl+click `Small_LLM_Model`;
2. Ctrl+click `ArgumentParser`;
3. hover over `encoded`;
4. type `encoded.` or Ctrl+click `tolist`.

After discussing this waypoint, return to prompt design for the next model
experiment.
