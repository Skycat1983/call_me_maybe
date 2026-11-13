"""Inspect the supplied LLM SDK through its public interface.

This learning probe was authored locally during Waypoints 006 and 007. It is
not part of the supplied SDK or project subject.
"""

from argparse import ArgumentParser
from collections.abc import Callable
from heapq import nlargest
from pathlib import Path
from time import perf_counter

from llm_sdk import Small_LLM_Model

PROMPT = "What is the sum of 2 and 3?"
TOP_CANDIDATE_COUNT = 10
# ? was this supplied to us or did we write it??
# Answer: We wrote both constants for this local learning probe. The prompt is
# deliberately simple, and ten candidates give a useful but readable sample.


def parse_device_argument() -> str | None:
    """Return an explicit SDK device choice, or ``None`` for automatic choice.

    An override is a value supplied by this script instead of allowing the SDK
    to select a device automatically. It is useful for controlled comparisons,
    such as changing only automatic selection to explicit CPU operation.
    """
    # ? what does this docstring mean here? what is the override?
    # Answer: It means this function may return a device chosen on the command
    # line. That explicit value overrides the SDK's automatic device selection.
    # ? is this necessary? A requirement? A safety net? Or something else?
    # Answer: It is not a project requirement. It is an experiment control and
    # currently a workaround: explicit CPU avoids the failing automatic CUDA
    # device-map path while leaving the supplied SDK implementation unchanged.
    # ? Under what circumstances would we want to supply this?
    # Answer: Supply it to reproduce behavior on known hardware, isolate a
    # device-specific failure, compare performance, or force a portable CPU
    # run.
    # ? what are device arguments? why is it useful?
    # Answer: They are command-line values such as `--device cpu`. They let us
    # compare hardware paths without editing the experiment's source code.
    # ? why is it useful to compare hardware paths?
    # Answer: CPU, CUDA, and MPS can take different loading branches, use
    # different dtypes and dependencies, and fail differently. Comparing one
    # controlled change helps identify which branch caused an observation.
    # ? what is __doc__?
    # Answer: At module level, `__doc__` contains the triple-quoted description
    # at the top of this file. argparse reuses it in the `--help` output.
    parser = ArgumentParser(description=__doc__)
    # ? why these specific arguments?
    # Answer: `--device` names the optional setting; `choices` rejects values
    # outside the three paths this experiment covers; and `help` explains the
    # option in the generated help screen. With no option, argparse returns
    # None, preserving the SDK's automatic-selection experiment.
    parser.add_argument(
        "--device",
        choices=("cpu", "cuda", "mps"),
        help="Pass an explicit device to Small_LLM_Model.",
    )
    return parser.parse_args().device


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
    requested_device = parse_device_argument()
    print_heading("Model construction")
    print("model identifier: Qwen/Qwen3-0.6B")
    print(f"requested device: {requested_device or 'automatic'}")

    construction_started = perf_counter()
    model = Small_LLM_Model(device=requested_device)
    construction_seconds = perf_counter() - construction_started
    print(f"construction time: {construction_seconds:.3f} seconds")

    print_heading("Encoding")
    encoded = model.encode(PROMPT)
    # ? how am i supposed to know there is a tolist method here?
    # Answer: You are not expected to guess it. `encode()` is annotated as
    # returning `torch.Tensor`, so editor hover/completion, Ctrl+click, runtime
    # `help(torch.Tensor.tolist)`, or the PyTorch docs reveal this method.
    # Selecting row zero gives one token sequence; `tolist()` converts it into
    # the ordinary list[int] expected by get_logits_from_input_ids().
    input_ids = encoded[0].tolist()
    print(f"prompt: {PROMPT!r}")
    # ? why do we have to convert this to a tuple?
    # Answer: We do not have to. `encoded.shape` is a torch.Size containing the
    # same dimensions. tuple(...) only prints the simpler form `(1, 11)` rather
    # than `torch.Size([1, 11])` in this diagnostic report.
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
