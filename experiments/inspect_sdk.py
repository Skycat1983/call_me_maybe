"""Inspect the supplied LLM SDK through its public interface."""

from collections.abc import Callable
from heapq import nlargest
from pathlib import Path
from time import perf_counter

from llm_sdk import Small_LLM_Model

PROMPT = "What is the sum of 2 and 3?"
TOP_CANDIDATE_COUNT = 10


def print_heading(title: str) -> None:
    """Print a visible section heading."""
    print(f"\n## {title}")


def inspect_tokenizer_file(
    label: str,
    path_getter: Callable[[], str],
) -> None:
    """Call a public SDK path method and report its result."""
    try:
        path = Path(path_getter())
        print(f"{label}: {path}")
        print(f"{label} exists: {path.is_file()}")
        if path.is_file():
            print(f"{label} size: {path.stat().st_size} bytes")
    except Exception as error:  # The experiment should report each failure.
        print(f"{label} error: {type(error).__name__}: {error}")


def main() -> None:
    """Run the public-interface SDK experiment."""
    print_heading("Model construction")
    print("model identifier: Qwen/Qwen3-0.6B")

    construction_started = perf_counter()
    model = Small_LLM_Model()
    construction_seconds = perf_counter() - construction_started
    print(f"construction time: {construction_seconds:.3f} seconds")

    print_heading("Encoding")
    encoded = model.encode(PROMPT)
    input_ids = encoded[0].tolist()
    print(f"prompt: {PROMPT!r}")
    print(f"tensor shape: {tuple(encoded.shape)}")
    print(f"tensor dtype: {encoded.dtype}")
    print(f"tensor device: {encoded.device}")
    print(f"token count: {len(input_ids)}")
    print(f"token IDs: {input_ids}")

    print_heading("Decoding")
    try:
        direct_decoded = model.decode(encoded)
        print(f"decode(encoded): {direct_decoded!r}")
    except Exception as error:
        print(
            "decode(encoded) error: "
            f"{type(error).__name__}: {error}"
        )

    try:
        row_decoded = model.decode(encoded[0])
        print(f"decode(encoded[0]): {row_decoded!r}")
    except Exception as error:
        print(
            "decode(encoded[0]) error: "
            f"{type(error).__name__}: {error}"
        )

    print_heading("Tokenizer files")
    inspect_tokenizer_file("vocabulary", model.get_path_to_vocab_file)
    inspect_tokenizer_file("merges", model.get_path_to_merges_file)
    inspect_tokenizer_file("tokenizer", model.get_path_to_tokenizer_file)

    print_heading("Next-token logits")
    logits_started = perf_counter()
    logits = model.get_logits_from_input_ids(input_ids)
    logits_seconds = perf_counter() - logits_started
    print(f"logit count: {len(logits)}")
    print(f"logits time: {logits_seconds:.3f} seconds")

    top_token_ids = nlargest(
        TOP_CANDIDATE_COUNT,
        range(len(logits)),
        key=logits.__getitem__,
    )
    for rank, token_id in enumerate(top_token_ids, start=1):
        token_text = model.decode([token_id])
        print(
            f"{rank:>2}. id={token_id:<7} "
            f"logit={logits[token_id]:>10.4f} "
            f"text={token_text!r}"
        )


if __name__ == "__main__":
    main()
