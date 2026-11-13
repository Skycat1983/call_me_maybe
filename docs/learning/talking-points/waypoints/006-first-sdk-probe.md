# Talking Points 006: First SDK Probe

Companion waypoint:
[006 — First SDK probe](../../waypoints/006-2026-11-10-first-sdk-probe.md)

## Agent preparation

Read:

- the companion waypoint;
- `experiments/inspect_sdk.py`;
- [known issues](../../../project/issues.md);
- [open questions](../../../project/questions.md).

Interpret the failure and choose the next controlled experiment. Do not
install `accelerate`, change SDK loading code, or redesign the application
during the voice session.

## Short recap

The environment imports the SDK, and a validated probe attempted the first
model construction. Transformers stopped during device-map handling because
`accelerate` was unavailable. Only small tokenizer/configuration metadata was
downloaded; encoding and logits were not reached.

## Key concepts to discuss

1. Import success versus constructor success.
2. Python dependencies versus model metadata versus model weights.
3. Sequential experiments and why one failure blocks later observations.
4. Broad version constraints and lockfile drift.
5. `device_map="auto"` and automatic device placement.
6. Missing dependency versus version incompatibility.
7. Hypothesis versus proven cause.
8. Controlled experiments that change one variable at a time.

## Evidence to review

| Evidence | Meaning |
|---|---|
| `llm_sdk` imports | The relocated environment is usable. |
| Constructor traceback | Failure is in model loading, not JSON or generation. |
| Error names `accelerate` | The active loading path requires that package. |
| Supplied lock uses Transformers 5.0.0 | Original environment differs from the root environment. |
| Root lock uses Transformers 5.20.2 | Broad constraints allowed version drift. |
| Both locks omit `accelerate` | Adding it changes the supplied dependency set. |
| Only 16 MB in HF cache | Large model weights did not load. |

## Discussion prompts

- Why does successful `import llm_sdk` not prove construction will work?
- At what stage did the probe stop?
- Which planned observations are still unavailable?
- What does `device_map="auto"` try to accomplish?
- What evidence supports a version-compatibility hypothesis?
- What evidence is still missing?
- Why might explicit CPU be a useful controlled test?
- Why might reproducing the supplied lock versions be useful?
- What are the risks of simply adding `accelerate`?
- Which option changes the fewest variables?
- Which result would justify changing dependency declarations?

## Candidate next experiments

### Option A: Current versions, explicit CPU

Change only the public constructor call:

```python
Small_LLM_Model(device="cpu")
```

This tests whether automatic device mapping caused the failure.

### Option B: Supplied dependency versions

Create a separate `/tmp` environment using the supplied SDK lock and rerun the
default constructor. This tests the version-drift hypothesis.

### Option C: Add `accelerate`

Add the requested dependency and rerun. This proves whether the missing
package is sufficient, but changes the dependency set and must be checked
against project restrictions.

### Option D: Small comparison matrix

Compare current versus supplied versions and default versus explicit CPU. This
provides the strongest evidence but requires more time and storage.

## Likely misconceptions

- An error can identify an immediate missing requirement without proving the
  best architectural fix.
- The newest compatible package version is not necessarily the supplied
  project's version.
- A nested lockfile is not automatically enforced by the root resolver.
- No generation conclusion can be drawn because inference never ran.
- Private `_device` state should not be inspected merely to debug this;
  public constructor arguments and external observations are available.
- Installing a package is an environment change that requires a reason beyond
  making an error disappear.

## Decision to reach

Choose the next controlled experiment and explain:

1. Which hypothesis it tests.
2. Which variable changes.
3. What outcome would support or reject the hypothesis.
4. Whether it changes dependencies or only experiment configuration.

## Voice-session review — 2026-11-13

This is a record of the *discussion*, not a new SDK experiment. It captures
where the learner paused, the explanations given, and what to recall unaided
next time. The original Waypoint 006 failure and the later Waypoint 007 CPU
success remain distinct events.

### Topics actually covered

1. **Purpose and limits of the first probe.** `inspect_sdk.py` was meant to
   construct the supplied wrapper, encode a prompt, compare decoding forms,
   locate tokenizer files, and request one next-token logit vector. In
   Waypoint 006 the default constructor failed; none of the later checks ran.
   Importing `llm_sdk` successfully proves less than successfully loading its
   model.
2. **Reading the traceback.** Python's frames identify a file path, line,
   and function; they trace calls from a caller to the exception site. The
   important diagnostic anchors are the application call site, the *last*
   library frame that raised the error, and the exception's type and message.
   Starting from the bottom is a practical way to identify the immediate
   failure before following the call chain upwards.
3. **Actual failure.** The captured final exception was `ValueError`, saying
   that using a `device_map`, `tp_plan`, `torch.device` context manager, or a
   non-default device setting required the separate `accelerate` package.
   The documented path was `Small_LLM_Model()` →
   `AutoModelForCausalLM.from_pretrained(...)` →
   `check_and_set_device_map(...)` → `ValueError`. This is evidence of the
   loading-path requirement, *not* an inference failure or a complete
   architectural diagnosis.
4. **Which file owns a line number.** The learner located a frame described
   as `line 137, in check_and_set_device_map` under
   `transformers/integrations/accelerate.py`. That is installed Transformers
   source, *not* line 137 of `experiments/inspect_sdk.py`. A traceback's
   filename and line number must be read together. The library file's name
   does not mean the separately distributed `accelerate` package was installed.
5. **Line-number discrepancy.** The learner reported an early frame at
   `line 125` in `inspect_sdk.py`, then could not find the expected code at
   that position. In the current `main` version reviewed on 2026-11-13, the
   constructor call is **line 92** and **line 125 is blank**. This is a
   concrete reason *not* to identify line 125 as the constructor in the
   currently published script. A traceback records the code and library
   locations for its particular run; source edits or changed environments
   may make later line numbers differ. We have not independently retrieved
   the exact historic terminal output or established why that particular
   frame reported 125.
6. **Device selection and controlled comparison.** The SDK's automatic
   device decision can enter a different loading path from explicit
   `device="cpu"`. The follow-up Waypoint 007 CPU experiment succeeded
   without installing `accelerate` or rewriting the SDK. This isolates a
   working CPU path, but does not fix default or GPU loading and does not
   prove which device was chosen in the failed process.
7. **Dependency drift remains a hypothesis, not a verdict.** The supplied
   lock recorded Transformers 5.0.0 and PyTorch 2.10.0; the root lock
   recorded Transformers 5.20.2 and PyTorch 2.14.1. Both omitted
   `accelerate`. A newer library version *may* affect compatibility, but no
   supplied-version comparison was performed in this discussion. The point
   of controlled experiments is to alter one relevant variable at a time.

### Learner observations and areas needing recall

- The learner actively found and read the final `ValueError` and identified
  the Transformers frame, rather than relying only on a summary.
- The main difficulty was deciding which traceback line and source file to
  inspect, especially after noticing multiple file paths and line numbers.
- Progress messages such as `tokenizer.json` reconstruction were initially
  distracting; they are not the final Python exception and do not themselves
  establish successful model construction.
- The CPU-workaround logic and the existence of a version mismatch were
  discussed, but have not yet been tested via unaided explanation.
- **Do not mark durable mastery as proven.** Begin the next discussion by
  asking for the explanations in the learner's own words, without giving the
  answer first.

### Targeted recall questions for the next voice session

Ask **one question at a time**, allowing an unaided answer before hints:

1. When reading a Python traceback, which three anchors are worth finding
   first? Where is the error *reason* usually stated?
2. What is the difference between the first relevant frame in your script
   and the final library frame raising the exception?
3. Why would `line 137` in `transformers/integrations/accelerate.py` not
   correspond to `line 137` in `inspect_sdk.py`?
4. What did the actual `ValueError` say, and what does it tell us without
   proving the best fix?
5. What is the difference between `import llm_sdk` succeeding and
   `Small_LLM_Model(...)` constructing successfully?
6. Why did encoding, decoding, and logits not execute in the failed default
   probe? What did the later CPU probe establish?
7. Why is `Small_LLM_Model(device="cpu")` a useful controlled test, and what
   does it *not* prove about default/GPU loading?
8. Which dependency versions differed between the supplied and root locks?
   Does that difference alone prove the cause?
9. If the old traceback says line 125 but current code shows a different
   line, how would you investigate without assuming the file is unchanged?
10. What experiment could separately test the version-compatibility
    hypothesis without casually changing production dependencies?

### Status and next discussion

**Covered during the call:** the first constructor failure; traceback
navigation and file ownership; the `accelerate` message; device selection;
the CPU comparison; lockfile drift; and the difference between an observed
requirement and a proven root cause.

**Still open:** exact reason the default run entered the failing path; the
production device/dependency policy (`I-003`, `Q-007`); and any controlled
supplied-version comparison. No code, dependencies, or model configuration
were changed during this voice review.

**Recommended sequence:** start the next session with the recall questions
above, then move to [Talking Points 007](007-explicit-cpu-sdk-probe.md) to
explain the successful tensor, decoding, tokenizer-file, and logits results.
For more detailed implementation-level explanation use the
[LLM-SDK theme](../themes/llm-sdk/index.md).

## Successful session outcome

The learner can explain the traceback's stage, distinguish competing
hypotheses, and choose a controlled follow-up without treating an unverified
workaround as the final solution.
