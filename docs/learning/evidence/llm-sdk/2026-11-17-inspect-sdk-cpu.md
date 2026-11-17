# Evidence: Explicit-CPU SDK Probe

- Captured: 2026-11-17
- Command: `make inspect-sdk-cpu` (inferred from the capture name and reported
  explicit CPU device)
- Model: `Qwen/Qwen3-0.6B`
- Device: CPU
- Capture type: Curated terminal transcript
- Exit status: Numeric status not recorded; successful return to the shell was
  observed
- Cache context: Hugging Face download and reconstruction progress appeared;
  the exact pre-run cache state was not independently recorded

## Why this capture is retained

This later run reproduced the important results from Waypoint 007:

- explicit-CPU construction completed;
- the prompt encoded to the same token IDs and tensor properties;
- batched and single-sequence decode returned the same container shapes;
- the same tokenizer files and sizes were reported;
- the logits vector again contained 151,936 scores;
- the same ten candidate token texts were ranked highest.

The timings differed from the earlier observation, which is expected for
runtime measurements and reinforces that they are observations rather than
guaranteed benchmarks.

## Curated terminal output

The source capture contained terminal-rendered progress bars that were already
truncated. They are represented by one omission marker below. The final shell
prompt was removed because it was not program output and exposed a local user,
host, and working-directory string.

```text
## Model construction
model identifier: Qwen/Qwen3-0.6B
requested device: cpu
Warning: You are sending unauthenticated requests to the HF Hub. Please set a HF_TOKEN to enable higher rate limits and faster downloads.
[Hugging Face download, reconstruction, and weight-loading progress omitted]
construction time: 19.244 seconds

## Encoding
prompt: 'What is the sum of 2 and 3?'
tensor shape: (1, 11)
tensor dtype: torch.int64
tensor device: cpu
token count: 11
token IDs: [3838, 374, 279, 2629, 315, 220, 17, 323, 220, 18, 30]

## Decoding
decode(encoded): ['What is the sum of 2 and 3?']
decode(encoded[0]): 'What is the sum of 2 and 3?'

## Tokenizer files
vocabulary: /tmp/call-me-maybe-huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca/vocab.json
vocabulary exists: True
vocabulary size: 2776833 bytes
merges: /tmp/call-me-maybe-huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca/merges.txt
merges exists: True
merges size: 1671853 bytes
tokenizer: /tmp/call-me-maybe-huggingface/hub/models--Qwen--Qwen3-0.6B/snapshots/c1899de289a04d12100db370d81485cdf75e47ca/tokenizer.json
tokenizer exists: True
tokenizer size: 11422654 bytes

## Next-token logits
logit count: 151936
logits time: 0.236 seconds
 1. id=3555    logit=   17.3810 text=' What'
 2. id=2014    logit=   16.7318 text=' To'
 3. id=7281    logit=   16.3472 text=' Also'
 4. id=4710    logit=   16.2304 text=' \n\n'
 5. id=2585    logit=   16.2256 text=' How'
 6. id=1597    logit=   15.9371 text=' And'
 7. id=2160    logit=   15.8764 text=' Is'
 8. id=220     logit=   15.8255 text=' '
 9. id=576     logit=   15.6270 text=' The'
10. id=2980    logit=   15.2162 text=' Can'
```

## Comparison with the earlier recorded run

| Observation | Waypoint 007 run | 2026-11-17 capture |
|---|---:|---:|
| Construction time | 18.419 seconds | 19.244 seconds |
| Logits time | 0.301 seconds | 0.236 seconds |
| Token count | 11 | 11 |
| Logit count | 151,936 | 151,936 |

Timing variation does not change the established behavior. This capture is not
a controlled benchmark because background load, cache state, and other runtime
conditions were not held constant.

## Related learning and source

- [Evidence index](../index.md)
- [Waypoint 007](../../waypoints/007-2026-11-12-explicit-cpu-sdk-probe.md)
- [Talking Points 007](../../talking-points/waypoints/007-explicit-cpu-sdk-probe.md)
- [LLM-SDK experiments and results](../../talking-points/themes/llm-sdk/probe/experiments-and-results.md)
- [`inspect_sdk.py`](../../../../experiments/inspect_sdk.py)
- [Experiment instructions](../../../../experiments/README.md)
