import pytest

from .data import TEST_DATA, TEST_DATA_RANDOM


def test_help(cli_invoke):
    result = cli_invoke(["--help"])
    assert result.exit_code == 0
    assert result.stdout.startswith("Usage: listSorting")


@pytest.mark.parametrize(
    "algorithm", ["iterator", "generator", "generator2", "generator3"]
)
@pytest.mark.parametrize("text_input, expected_output", TEST_DATA + TEST_DATA_RANDOM)
def test_algorithm(
    algorithm: str, text_input: str, expected_output: str, cli_invoke, tmp_path
):
    test_input_file = tmp_path / "input.txt"
    test_input_file.write_text(text_input)
    test_output_file = tmp_path / "output.txt"
    result = cli_invoke(
        [
            "--algorithm",
            algorithm,
            str(test_input_file.resolve()),
            str(test_output_file.resolve()),
        ]
    )

    assert result.exit_code == 0
    assert test_output_file.read_text() == expected_output
