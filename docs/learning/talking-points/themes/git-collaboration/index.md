# Theme: Git Collaboration and Branch Reconciliation

- Kind: Thematic talking-point index
- Status: Living
- Last reviewed: 2026-11-17
- Prerequisites: Basic working tree, commit, branch, remote, pull, and push

## Files to have open

- [`AGENTS.md`](../../../../../AGENTS.md) — the repository rule to inspect the working tree and preserve other contributors' changes.
- [Waypoint 001](../../../waypoints/001-2026-11-06-repository-and-source-files.md) — the original repository and remote setup in chronological context.
- [Talking points 001](../../waypoints/001-repository-and-source-files.md) — the foundational Git concepts that precede branch reconciliation.
- [Project status](../../../../project/status.md) — the current project state to compare with Git history before changing it.

## Purpose

Use this theme when local `main` and GitHub's `origin/main` both contain new
commits. It explains why Git calls this a divergence, how to inspect both
sides, when rebase is appropriate, how conflicts are resolved, and why a
successful reconciliation often needs no force push.

## Five-minute mental model

Two commits can share the same parent without containing each other:

```text
             local commit ea11dd7
            /
base 4ff18ba
            \
             remote commit dd9d7df
```

Local `main` was therefore one commit ahead and one commit behind
`origin/main`. A normal push could not discard the remote commit, and Git
needed an explicit policy before `pull` could combine the histories.

The chosen rebase produced:

```text
base 4ff18ba
    -> remote voice-review commit dd9d7df
    -> rebased local evidence commit 9be2e3d
```

The content of the local commit stayed intact, but its hash changed because a
commit hash includes its parent.

## What the failed pull actually did

The command was:

```bash
git pull --tags origin main
```

`git pull` has two conceptual stages:

```text
fetch remote objects and update origin/main
    -> integrate origin/main into the current branch
```

The fetch stage succeeded and moved `origin/main` from `4ff18ba` to
`dd9d7df`. The integration stage stopped because the branches diverged and no
merge/rebase policy was configured.

The `--tags` option also fetches tags. It did not cause or resolve the branch
divergence.

## Diagnose before changing history

Run:

```bash
git status --short --branch
git fetch origin
git log --oneline --decorate --graph --all -16
git log --oneline --left-right --cherry-pick main...origin/main
```

Read the results as follows:

- `ahead 1`: one local commit is absent from `origin/main`;
- `behind 1`: one remote commit is absent from local `main`;
- `<`: a commit belongs only to the left side, local `main`;
- `>`: a commit belongs only to the right side, `origin/main`.

Then compare changed paths:

```bash
git diff --name-status origin/main..main
git show --stat <local-commit>
git show --stat <remote-commit>
```

This predicts whether Git can combine the work automatically. In the recorded
case, the local commit added evidence and the remote commit added Talking
Points 011 review notes. They did not edit the same lines.

## The three pull policies

### Rebase

```bash
git pull --rebase origin main
```

or, after a separate fetch:

```bash
git rebase origin/main
```

Rebase temporarily removes local-only commits, advances the branch to the
remote commit, then reapplies the local commits. It creates a linear history
and changes the hashes of the reapplied commits.

Use it when local-only commits have not already been shared with other people
or systems. This matched the recorded situation.

### Merge

```bash
git pull --no-rebase origin main
```

Merge preserves both existing commit identities and adds a merge commit with
two parents. It is appropriate when history must not be rewritten or when the
local commits are already shared.

### Fast-forward only

```bash
git pull --ff-only origin main
```

This succeeds only if local `main` has no independent commits. It is a useful
safety policy because it refuses to choose merge or rebase automatically, but
it cannot itself resolve a divergence.

## Recommended workflow for this repository

Because remote agents may add commits between local work sessions:

```bash
git status --short --branch
git fetch origin
git log --oneline --left-right --cherry-pick main...origin/main
git rebase origin/main
git push origin main
```

Before rebasing, the working tree should normally be clean. Commit completed
work first, or deliberately stash unfinished work and remember that the stash
must later be reapplied and checked.

The optional repository-local preference is:

```bash
git config pull.rebase true
```

Without `--global`, this affects only the current repository. It changes the
default integration policy; it does not remove the need to inspect what local
and remote agents changed.

## Conflict workflow

If rebase stops on a conflict:

```bash
git status
```

Open each conflicted file and find markers resembling:

```text
<<<<<<<
local or current content
=======
other content
>>>>>>>
```

Create the correct combined content, remove all markers, then run:

```bash
git add <resolved-files>
git rebase --continue
```

Repeat if another commit conflicts. To return to the exact pre-rebase state:

```bash
git rebase --abort
```

Do not choose one side blindly when both agents added useful notes. Read the
purpose of each change and preserve both where compatible.

## Why no force push was needed

After rebase, local history contained the remote commit followed by the
rebased local commit. GitHub could therefore advance normally:

```text
dd9d7df -> 9be2e3d
```

The normal command worked:

```bash
git push origin main
```

A force push would have been unnecessary and riskier. If rewritten history
ever genuinely must replace an already-published branch, stop and coordinate
first; `--force-with-lease` is safer than `--force`, but neither was required
here.

## Recorded example

| Role | Commit | Content |
|---|---|---|
| Shared base | `4ff18ba` | Earlier synchronized project state |
| Local-only before rebase | `ea11dd7` | Waypoint/evidence organization work |
| Remote-only | `dd9d7df` | Talking Points 011 voice-review notes |
| Rebased local commit | `9be2e3d` | Same local content, new parent and hash |

The final branch preserved both commits and pushed as a fast-forward.

## Voice-session guidance

Ask the agent to let the learner draw the commit graph before naming a
solution. Then discuss one boundary at a time:

1. working tree changes versus committed changes;
2. local `main` versus remote-tracking `origin/main`;
3. fetch versus integration;
4. merge versus rebase versus fast-forward only;
5. automatic combination versus a content conflict;
6. ordinary push versus force push.

## Recall questions

- What does `ahead 1, behind 1` mean?
- Why can a fetch succeed while the pull still fails?
- Did `--tags` cause this divergence?
- Why did rebasing change `ea11dd7` into `9be2e3d`?
- Why was rebase appropriate for an unpublished local commit?
- When would merge be safer than rebase?
- What does `git rebase --abort` guarantee?
- Why should conflicts be resolved by intent rather than by choosing “ours”
  or “theirs” automatically?
- Why did the final push not require `--force`?
- What does `git config pull.rebase true` change, and what does it not change?

## Successful discussion outcome

The learner can read a divergent graph, identify which commits exist on each
side, choose and justify a reconciliation policy, describe the conflict
workflow, and explain why the recorded result preserved both agents' work.

## Related learning

- [Talking-points hub](../../index.md)
- [Thematic discussions](../index.md)
- [Talking Points 001: repository and source files](../../waypoints/001-repository-and-source-files.md)
- [Waypoint 001](../../../waypoints/001-2026-11-06-repository-and-source-files.md)
- [Python project tooling](../python-tooling/index.md)
- [Project status](../../../../project/status.md)
- [Repository agent instructions](../../../../../AGENTS.md)
