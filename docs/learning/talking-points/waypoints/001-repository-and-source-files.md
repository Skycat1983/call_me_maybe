# Talking Points 001: Repository and Source Files

Companion waypoint:
[001 — Repository and source files](../../waypoints/001-2026-11-06-repository-and-source-files.md)

## Agent preparation

Read the companion waypoint before the discussion. Focus on Git concepts and
the difference between source files, ignored local artifacts, and transport
archives. Do not turn the session into a Git command exercise unless asked.

## Short recap

The existing workspace became a Git repository connected to GitHub. The
supplied ZIP archives were extracted, source files were committed, and the PDF
remained local through `.gitignore`. The ZIP files were deleted after their
contents were verified.

## Key concepts to discuss

1. Working tree, staging area, commit, branch, remote, and push.
2. What `.gitignore` does and does not do.
3. Local-only files versus repository files.
4. Why source should be committed in an inspectable form.
5. Why a ZIP is a transport artifact rather than useful source history.
6. Why `git status` is an important safety check.

## Discussion prompts

<!-- - Explain the journey of a file from the workspace to GitHub. -->
<!-- - What is the difference between `git add`, `git commit`, and `git push`? -->
<!-- - Why did the PDF remain on disk after being ignored? -->
<!-- - Why was `.gitignore` added before the first `git add`? -->
- Why were the extracted files preferable to committing only the ZIPs?
- When would keeping an original archive still be justified?
- What did setting `origin` accomplish?
- What does `main` represent locally and remotely?

## Understanding checks

Ask the learner to predict:

<!-- - Whether `.gitignore` deletes a file. -->
- Whether an already tracked file becomes untracked merely by adding it to
  `.gitignore`.
- Whether a commit automatically appears on GitHub.
- What `git status --ignored --short` should show for the local PDF.

## Likely misconceptions

<!-- - `.gitignore` does not delete files. -->
<!-- - `.gitignore` does not retroactively remove already tracked files. -->
- A commit is local until it is pushed.
- A Git remote is a named destination, not a second local copy of the working
  directory.
- Extracting an archive does not prove the extraction is complete; contents
  should be listed or otherwise verified before deletion.

## Successful session outcome

The learner can describe the Git flow in their own words and explain why the
PDF stayed local while the extracted project files became reviewable Git
history.
