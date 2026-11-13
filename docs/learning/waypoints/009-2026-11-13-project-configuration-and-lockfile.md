# Waypoint 009: Project Configuration and Lockfile

- Date: 2026-11-13
- Stage: Development tooling and dependency management
- Status: Complete

Voice discussion:
[Talking points 009](../talking-points/waypoints/009-project-configuration-and-lockfile.md)

## Purpose

Explain which project dependency information humans authored, which
information uv generated, how the choices were justified, and what
`make install` does with both files.

## The central distinction

`pyproject.toml` and `uv.lock` have different authors and different jobs:

```text
project requirements + supplied package metadata + development decisions
                              |
                              v
                    human-authored pyproject.toml
                              |
                       uv resolves graph
                              v
                       generated uv.lock
                              |
                         uv sync
                              v
              reproducible installed environment
```

We decided what the project directly requires. uv calculated the complete
set of direct and transitive packages needed to satisfy those declarations.

## How `pyproject.toml` was created

The root file was authored locally; it was not generated from the PDF or
copied from the SDK. Its entries came from several sources.

### Required project metadata

The name, initial `0.1.0` version, description, and README path are ordinary
metadata chosen for this new local project.

The project subject explicitly requires Python 3.10 or later, producing:

```toml
requires-python = ">=3.10"
```

### Runtime dependencies

The subject explicitly requires:

- the supplied `llm-sdk` package;
- NumPy;
- Pydantic, including use of Pydantic for project classes.

They became the root direct dependencies:

```toml
dependencies = [
    "llm-sdk",
    "numpy>=1.26",
    "pydantic>=2.0",
]
```

The subject required NumPy and Pydantic but did not prescribe these exact
minimum versions. The lower bounds were project choices selecting modern,
Python-3.10-compatible APIs. They are constraints, not the final installed
versions.

The supplied SDK already has its own `pyproject.toml`, declaring:

```text
torch >= 2.0.0
transformers >= 4.40.0
huggingface-hub >= 0.20.0
```

Those are transitive dependencies of the root project. They do not need to be
duplicated in the root dependency list merely because `llm_sdk` imports them.

### Local SDK source

Declaring `"llm-sdk"` says the package is required. This separate table says
where uv must obtain it:

```toml
[tool.uv.sources]
llm-sdk = { path = "llm_sdk" }
```

Without the source entry, uv would look for a package with that name through
its configured package index rather than use the supplied directory.

### Development dependencies

The subject requires Flake8 and Mypy commands. pytest was added as the chosen
test runner because tests are strongly recommended. They are development
tools rather than imports required by the running application, so they belong
in a development dependency group.

Their exact lower bounds were project choices, not fixed by the subject.

### uv storage settings

The `[tool.uv]` cache and link settings were later added after storage
experiments showed that large package data must stay off the small home
filesystem. They configure uv itself rather than becoming installed Python
dependencies.

## How `uv.lock` was created

We did not decide and type all 102 locked packages manually.

The first `uv sync`—or an explicit `uv lock`—read:

1. the root direct dependencies and allowed version ranges;
2. the local SDK's dependency declarations;
3. every selected package's dependencies;
4. the supported Python range and platform markers;
5. available package versions and distribution metadata.

uv solved those constraints, selected a compatible graph, and wrote
`uv.lock`. The file records exact resolved versions and distribution metadata
so later synchronization does not need to make fresh version choices.

The lockfile is generated project data that should be committed, but it should
not normally be hand-edited. To change dependencies, edit `pyproject.toml` and
ask uv to update the resolution.

## What `uv sync` does

For this repository, `make install` runs:

```text
uv sync
```

The command:

1. reads `pyproject.toml`;
2. checks whether `uv.lock` still matches those declarations;
3. updates the resolution when necessary;
4. creates the configured virtual environment when absent;
5. installs the locked packages into that environment;
6. removes extraneous packages when needed so the environment matches the
   project definition.

The Makefile exports `UV_PROJECT_ENVIRONMENT`, so the environment is created
at `/tmp/call-me-maybe-venv` rather than as a large directory in the
repository.

## Makefile questions answered

Inline answers now explain:

- `UV_PROJECT_ENVIRONMENT` is the virtual-environment location;
- `UV_CACHE_DIR` contains disposable package downloads and extracted data;
- `HF_HOME` is recognised by Hugging Face and was placed on the large
  filesystem for model/tokenizer storage;
- `UV_LINK_MODE=copy` makes installed files independent from uv cache files;
- `export` passes Make variables to recipe processes;
- `unexport VIRTUAL_ENV` removes that variable only from recipe environments,
  not from the caller's shell;
- `uv sync` reconciles declarations, lock data, and the installed environment.

## SDK probe questions answered

The learner's `# ?` comments remain in `experiments/inspect_sdk.py`. Answers
now immediately explain:

- the prompt and candidate-count constants were locally authored;
- the meaning and usefulness of a device override;
- command-line device arguments;
- the module `__doc__` attribute;
- each `ArgumentParser.add_argument()` value;
- how a learner can discover `Tensor.tolist()`;
- why converting `torch.Size` to a tuple is optional display formatting.

The real function docstring for `parse_device_argument()` was also expanded.
No standalone triple-quoted expressions were inserted merely to imitate
docstrings; those would execute as unused string expressions rather than serve
as Python documentation.

## Validation

The following checks passed:

```text
make -n install       -> uv sync
uv lock --check       -> resolved 102 packages
flake8 inspect_sdk.py -> no findings
git diff --check      -> no whitespace errors
```

## TOML editor readability

The TOML files initially appeared as uniformly white text in VS Code. This was
an editor-language-support problem rather than a reason to add more structural
noise to the files: no TOML extension was installed, so the editor lacked the
grammar needed to classify comments, table headers, keys, and values.

Even Better TOML `0.21.2` was installed. It registers both `*.toml` and
`uv.lock`, and provides syntax highlighting, validation, folding, navigation,
and formatting. It occupies approximately 69 MB; home usage remained at 78%
with approximately 1.1 GB available after installation.

VS Code must reload once after installation. The existing Monokai theme can
then assign different colors to the TOML token categories. If the resulting
comment color is still too dim, that color can be adjusted separately through
`editor.tokenColorCustomizations`; it should be evaluated visually before
adding a project-specific override.

## Decisions

- Keep learner questions in their original `# ?` form.
- Put concise answers immediately below them.
- Use real Python docstrings for functions and classes, and comments for
  line-level explanations.
- Treat `pyproject.toml` as the human intent and `uv.lock` as uv's resolved
  record.
- Change dependency intent in TOML, then regenerate the lock; do not edit the
  dependency graph directly in the lockfile.
- Use TOML language support for visual separation instead of making generated
  lockfiles more verbose or manually reformatting them.

## Next step

Use the companion talking points to explain the configuration-to-environment
chain in the learner's own words. Then continue inspecting the SDK probe and
return to the prompt-design experiment.
