"""Tests for command-line path parsing and input-error presentation."""

from pathlib import Path

import pytest

from src.cli import (
    DEFAULT_FUNCTION_DEFINITIONS_PATH,
    DEFAULT_INPUT_PATH,
    DEFAULT_OUTPUT_PATH,
    main,
    parse_args,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
INPUT_DIRECTORY = PROJECT_ROOT / "data" / "input"


def test_parse_args_uses_documented_default_paths() -> None:
    """Use the subject's three paths when no flags are supplied."""

    paths = parse_args([])

    assert paths.functions_definition == DEFAULT_FUNCTION_DEFINITIONS_PATH
    assert paths.input == DEFAULT_INPUT_PATH
    assert paths.output == DEFAULT_OUTPUT_PATH


def test_parse_args_accepts_explicit_path_overrides() -> None:
    """Convert each explicit path argument into a Path object."""

    paths = parse_args(
        [
            "--functions_definition",
            "custom/functions.json",
            "--input",
            "custom/prompts.json",
            "--output",
            "custom/results.json",
        ]
    )

    assert paths.functions_definition == Path("custom/functions.json")
    assert paths.input == Path("custom/prompts.json")
    assert paths.output == Path("custom/results.json")


def test_help_exits_successfully(capsys: pytest.CaptureFixture[str]) -> None:
    """Let argparse display help and use its conventional zero exit code."""

    with pytest.raises(SystemExit) as caught:
        parse_args(["--help"])

    assert caught.value.code == 0
    assert "--functions_definition PATH" in capsys.readouterr().out


def test_unknown_argument_uses_argparse_error_exit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Let argparse reject unknown syntax with exit code two."""

    with pytest.raises(SystemExit) as caught:
        parse_args(["--unknown"])

    assert caught.value.code == 2
    assert "unrecognized arguments" in capsys.readouterr().err


def test_missing_argument_value_uses_argparse_error_exit(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Let argparse reject a path flag that has no value."""

    with pytest.raises(SystemExit) as caught:
        parse_args(["--input"])

    assert caught.value.code == 2
    assert "expected one argument" in capsys.readouterr().err


def test_main_validates_explicit_inputs_without_writing_output(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Return success after validation without inventing output records."""

    output_path = tmp_path / "function_calls.json"
    exit_code = main(
        [
            "--functions_definition",
            str(INPUT_DIRECTORY / "functions_definition.json"),
            "--input",
            str(INPUT_DIRECTORY / "function_calling_tests.json"),
            "--output",
            str(output_path),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 0
    assert captured.out == ""
    assert captured.err == ""
    assert not output_path.exists()


def test_main_reports_input_error_without_traceback(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Present an expected loader failure on stderr with exit code one."""

    exit_code = main(
        [
            "--functions_definition",
            str(INPUT_DIRECTORY / "functions_definition.json"),
            "--input",
            str(tmp_path / "missing.json"),
            "--output",
            str(tmp_path / "output.json"),
        ]
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert captured.out == ""
    assert captured.err.startswith("error: Could not read")
    assert "Traceback" not in captured.err


def test_main_does_not_hide_unexpected_errors(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Allow programming errors outside InputLoadError to remain visible."""

    def fail_unexpectedly(path: str | Path) -> None:
        raise RuntimeError("unexpected failure")

    monkeypatch.setattr("src.cli.load_prompts", fail_unexpectedly)

    with pytest.raises(RuntimeError, match="unexpected failure"):
        main([])
