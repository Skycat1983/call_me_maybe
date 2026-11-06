# Constrained Decoding Requirements

Status: Active  
Source: Call Me Maybe subject, version 1.7

## Purpose

Small language models do not reliably produce structured output through prompting alone. The project must constrain generation token by token so every completed result is valid JSON and conforms to an available function schema.

Prompting the model to produce JSON and validating only after generation does not satisfy this requirement.

## Required generation loop

For each generated token:

1. Encode the current prompt and generated prefix as input IDs.
2. Obtain next-token logits from the LLM.
3. Determine which vocabulary tokens preserve a valid partial JSON document.
4. Further restrict those tokens to the schema allowed at the current output position.
5. Set the logits of invalid tokens to negative infinity.
6. Select a token only from the valid candidates.
7. Append it and repeat until the structured response is complete.

Generated tokens become part of the next model input.

## Syntax constraints

The decoder must preserve JSON validity while generating:

- Object delimiters.
- Property names.
- Colons and commas.
- Strings and escape sequences.
- Numbers.
- Booleans and other supported parameter types.
- Valid termination without trailing content or trailing commas.

A candidate may contain more than one character or fragment. It is valid only when its complete decoded text can be consumed without making the partial document impossible to complete.

## Schema constraints

The decoder must enforce the supplied function definitions:

- The generated function name must be one of the available names.
- Parameter keys must belong to the selected function.
- Every required parameter must be generated.
- No extra parameter may be generated.
- Each value must match its declared type.
- The completed structure must match the required output representation.

For example, a parameter declared as `number` must remain compatible with a valid JSON number throughout generation and resolve to a numeric value.

## Function selection

The LLM must decide which available function best matches the prompt.

The constrained decoder may restrict the generated name to names present in the definitions. It must not choose the function through keyword rules, direct mappings, or other non-LLM heuristics.

This separates two responsibilities:

- The LLM ranks semantically appropriate choices.
- The decoder prevents structurally or schematically invalid choices.

## Tokenization considerations

Tokenization uses subword units rather than simple words. A vocabulary token may contain:

- A leading-space marker.
- Punctuation.
- Part of a property name or value.
- Multiple characters or structural symbols.
- Encoded byte or Unicode fragments.

Use the SDK vocabulary path to map token IDs to their string representations when evaluating candidates. Do not assume one token equals one character or word.

## Required SDK boundary

Use public methods from the supplied `Small_LLM_Model`, including as needed:

```python
get_logits_from_input_ids(input_ids: list[int]) -> list[float]
get_path_to_vocab_file() -> str
encode(text: str)
decode(token_ids: list[int]) -> str
```

`decode` is optional. Private SDK state and methods are forbidden.

## Success conditions

The constrained-decoding layer succeeds only when:

- Every emitted result can be parsed as JSON.
- Every result conforms to the chosen function schema.
- Invalid candidate tokens cannot be selected.
- Function selection still comes from the LLM's scores.
- Behavior is not hardcoded to the demonstration data.
