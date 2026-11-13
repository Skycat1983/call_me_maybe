# Runtime Flow: Tokenizer Files

- Kind: Thematic talking point
- Theme: LLM SDK and `inspect_sdk`
- Depth: Detailed execution stage 11
- Status: Living
- Last reviewed: 2026-11-13
- Prerequisites: [Encoding and decoding](encoding-and-decoding.md)

## Stage 11: Inspect tokenizer files

The script calls one helper three times:

```python
inspect_tokenizer_file("vocabulary", model.get_path_to_vocab_file)
inspect_tokenizer_file("merges", model.get_path_to_merges_file)
inspect_tokenizer_file("tokenizer", model.get_path_to_tokenizer_file)
```

Notice that the script passes each method without parentheses. It passes a
bound method object; the helper decides when to call it.

### Helper variables

| Variable | Type | Example meaning |
|---|---|---|
| `label` | `str` | `"vocabulary"` for printed output |
| `path_getter` | `Callable[[], str]` | Bound method needing no further argument |
| `path` | `Path` | Object wrapping returned filesystem text |
| `error` | `Exception` | Exists only if that getter/check fails |

`Callable[[], str]` means: “a callable receiving no arguments and returning a
string.” `self` is already attached because this is a bound instance method.

### Inside each SDK getter

The vocabulary method first asks the tokenizer metadata for the configured
file name, falling back to `vocab.json`:

```text
vocab_file_name
type: str
role: repository filename
```

It then calls `hf_hub_download(repo_id=..., filename=...)`. Despite its name,
that function can reuse an already cached file and returns a local path string.

The same pattern applies to:

```text
merges_file_name       fallback merges.txt
tokenizer_file_name    fallback tokenizer.json
```

### Back in the helper

`Path(path_getter())` converts the returned string to a `Path`. The helper
checks whether it is a file and prints its byte size.

Observed files:

| Artifact | Observed size |
|---|---:|
| `vocab.json` | 2,776,833 bytes |
| `merges.txt` | 1,671,853 bytes |
| `tokenizer.json` | 11,422,654 bytes |

The files are model/tokenizer data, not Python dependencies.

## Related learning

- [Runtime-flow map](index.md)
- [Previous: encoding and decoding](encoding-and-decoding.md)
- [Next: logits and ranking](logits-and-ranking.md)
- [SDK reference](../../../../../reference/llm-sdk.md)

