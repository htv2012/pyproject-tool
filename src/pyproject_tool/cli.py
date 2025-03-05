import click

from .pytest_log import pytest_log


@click.group()
@click.version_option()
def main() -> None:
    pass


main.add_command(pytest_log)
