# Open Questions

This register contains only unresolved questions. Answered questions remain in
the waypoint where they were discussed.

## Q-004: What prompt format produces reliable semantic function selection?

- Status: Open
- Opened: Waypoint 004
- Theme: Model integration

The LLM must see the user request and available function descriptions, but the
exact prompt structure has not been designed.

This must be answered experimentally. The design may format definitions for
the model, but it may not replace model selection with keyword heuristics.

## Q-005: How should a per-prompt generation failure be represented?

- Status: Open
- Opened: Requirements review
- Theme: Error handling

The subject requires clear, graceful errors but defines no output schema for a
prompt that cannot be mapped successfully. The normal output object permits
exactly `prompt`, `name`, and `parameters`.

Next step: keep file-level errors separate from successful output and record a
design decision before implementing per-prompt failure behavior.

## Q-007: What device and dependency policy should production use?

- Status: Open
- Opened: [Waypoint 007](../learning/waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)
- Theme: SDK dependencies and device loading

Explicit CPU construction succeeds without `accelerate`, while the observed
default loading path fails when Transformers requests device mapping.

The next design decision must distinguish:

- using explicit CPU for correctness and portability;
- supporting automatic CUDA loading by declaring `accelerate`;
- restoring supplied dependency versions;
- allowing a documented device setting through the application.

The decision should be based on project rules, evaluator hardware, measured
performance, and whether GPU support is mandatory.
