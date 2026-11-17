# Learning Evidence

This directory contains curated primary evidence from meaningful commands and
experiments. Evidence records what a process actually printed or returned;
waypoints explain what happened during a stage, and thematic talking points
explain what the result means.

## Available evidence

| Date | Subject | Capture | Related learning |
|---|---|---|---|
| 2026-11-17 | Successful explicit-CPU SDK probe | [Terminal capture](llm-sdk/2026-11-17-inspect-sdk-cpu.md) | [Waypoint 007](../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md), [LLM-SDK results](../talking-points/themes/llm-sdk/probe/experiments-and-results.md) |

## What belongs here

Retain a capture when it provides useful evidence for at least one of these:

- a meaningful experiment or comparison;
- a reproducible failure or repair;
- an important runtime or performance observation;
- an external tool result that supports a project decision;
- output that a future discussion agent should inspect directly.

Routine repeated test, lint, or installation output does not need to be
committed. Keep disposable output under `/tmp` unless it supports a durable
learning or project record.

## Capture format

Each retained file should state:

- the capture date;
- the command, including whether it was directly recorded or inferred;
- the relevant environment, model, or device;
- whether the exit status was recorded;
- whether output is raw or curated;
- omissions such as terminal-rendered progress bars;
- related source, waypoint, thematic guide, issue, or question.

Use a fenced `text` block for command output. Remove the interactive shell
prompt, terminal control characters, and unrelated noise. Never retain access
tokens, credentials, private environment variables, or other secrets.

## Evidence versus interpretation

```text
evidence capture   what the command displayed
waypoint           what happened and why it mattered then
thematic guide     the current reusable explanation
talking points     how to discuss and test understanding
```

If a later run differs, preserve both observations with dates. Do not replace
a historical value as though the earlier run never occurred.

## Related learning

- [Learning and progress log](../index.md)
- [Talking-points hub](../talking-points/index.md)
- [Documentation index](../../index.md)
