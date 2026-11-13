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

## Successful session outcome

The learner can explain the traceback's stage, distinguish competing
hypotheses, and choose a controlled follow-up without treating an unverified
workaround as the final solution.
