# Waypoint 001: Repository and Source Files

Date: 2026-11-06  
Stage: Project foundation  
Status: Complete

## Purpose

Place the supplied project materials in a personal GitHub repository while
keeping the subject PDF local and untracked.

## Topics covered

- Initializing Git in an existing workspace.
- Connecting a local repository to a new GitHub remote.
- Using `.gitignore` for local-only files.
- Extracting supplied archives before versioning their contents.
- Distinguishing source files from transport archives.

## Progress made

- Initialized the workspace as a Git repository.
- Created the `main` branch.
- Connected `origin` to
  `git@github.com:Skycat1983/call_me_maybe.git`.
- Extracted `data.zip` and `llm_sdk.zip`.
- Added the extracted data and SDK files.
- Added a root README and `.gitignore`.
- Kept `call_me_maybe.pdf` out of Git.
- Initially kept both ZIP files local and ignored.
- Created and pushed commit `3167287` (`Initial commit`).
- Deleted the ZIP files after verifying their extracted contents.

## Questions and answers

### How do existing workspace files become part of the new repository?

Initialize Git in the workspace, add an ignore file before staging, inspect the
staged set, commit it, connect the remote, and push `main`. The important
safety step is checking `git status` before the first commit.

### How can the PDF remain local without being pushed?

Add its exact filename to `.gitignore` before staging:

```gitignore
call_me_maybe.pdf
```

An ignored file remains on disk but is absent from commits. `git status
--ignored --short` shows it with the `!!` marker.

### Should the ZIP archives be committed?

No. Once extraction was verified, the archives contained no information that
was not already present in `data/` and `llm_sdk/`. Keeping both forms would
duplicate content and make the repository less convenient to review.

### Why stage extracted files rather than only the archives?

Git can display, compare, and review source files directly. A ZIP is an opaque
binary artifact: small changes replace the whole archive and hide the actual
source diff.

## Evidence and experiments

The extracted files were listed before deleting the archives:

```text
data/input/function_calling_tests.json
data/input/functions_definition.json
llm_sdk/llm_sdk/__init__.py
llm_sdk/pyproject.toml
llm_sdk/uv.lock
```

After the first push, the local branch and `origin/main` both pointed to
commit `3167287`.

## Decisions

- Track extracted project content.
- Ignore the PDF permanently unless requirements change.
- Remove redundant ZIP archives after extraction.
- Use SSH for the GitHub remote.

## Open questions or issues

None remained from this waypoint.

## Documents created or updated

- `.gitignore`
- `README.md`

## Next step

Extract the subject's requirements into searchable Markdown documentation.
