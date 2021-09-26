import functools

import pytest
from typer import Typer
from typer.testing import CliRunner


@pytest.fixture
def cli_entrypoint() -> Typer:
    """See: https://typer.tiangolo.com/tutorial/testing/#test-a-function"""
    from list_sorting.cli import list_sorting

    app = Typer()
    app.command(name="listSorting")(list_sorting)

    return app


@pytest.fixture
def cli_invoke(cli_entrypoint):
    runner = CliRunner()
    return functools.partial(runner.invoke, cli_entrypoint)
