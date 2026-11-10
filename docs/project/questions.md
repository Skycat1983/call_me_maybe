# Open Questions

This register contains only unresolved questions. Answered questions remain in
the waypoint where they were discussed.

## Q-001: Does SDK decode accept the direct result of encode?

Status: Open  
Opened: Waypoint 004  
Theme: Tokenization

`encode()` returns a two-dimensional tensor shaped `[1, token_count]`, while
the underlying tokenizer normally expects a one-dimensional sequence in
`decode()`.

Experiment to run:

```python
encoded = model.encode("hello")
model.decode(encoded)
model.decode(encoded[0])
```

Record which calls work and whether both reconstruct the original text.

## Q-002: Which parameter schema types must be supported?

Status: Open  
Opened: Waypoint 004  
Theme: Input schema

The demonstration definitions use only `string` and `number`. The subject also
mentions `boolean` and says the evaluation files may change.

Next step: derive the minimum mandatory type set from the subject and later
test replacement definitions containing each supported type.

## Q-003: Which tokenizer files are available for Qwen3?

Status: Open  
Opened: Waypoint 004  
Theme: Tokenization

The SDK exposes paths for vocabulary, merges, and complete tokenizer files,
but their actual filenames and formats are determined at runtime by the Qwen
tokenizer.

Next step: after dependencies and model files are available, call each public
path method and inspect the returned file without accessing private SDK state.

## Q-004: What prompt format produces reliable semantic function selection?

Status: Open  
Opened: Waypoint 004  
Theme: Model integration

The LLM must see the user request and available function descriptions, but the
exact prompt structure has not been designed.

This must be answered experimentally. The design may format definitions for
the model, but it may not replace model selection with keyword heuristics.

## Q-005: How should a per-prompt generation failure be represented?

Status: Open  
Opened: Requirements review  
Theme: Error handling

The subject requires clear, graceful errors but defines no output schema for a
prompt that cannot be mapped successfully. The normal output object permits
exactly `prompt`, `name`, and `parameters`.

Next step: keep file-level errors separate from successful output and record a
design decision before implementing per-prompt failure behavior.
