import pathlib

import click
import tomli_w
import tomllib


def update_config(config: dict):
    pytest_ini = (
        config.setdefault("tool", {})
        .setdefault("pytest", {})
        .setdefault("ini_options", {})
    )
    log_defaults = {
        "log_cli": True,
        "log_cli_level": "DEBUG",
        "log_cli_format": "%(levelname)-8s | %(name)s:%(message)s",
        "log_cli_date_format": "%Y-%m-%d %H:%M:%S",
        "log_file": "pytest.log",
        "log_file_level": "DEBUG",
        "log_file_format": "%(levelname)-8s | %(name)s:%(message)s",
        "log_file_date_format": "%Y-%m-%d %H:%M:%S",
    }
    for key, value in log_defaults.items():
        pytest_ini.setdefault(key, value)


def add_pytest_log(file):
    with open(file, "rb") as stream:
        config = tomllib.load(stream)

    update_config(config)

    with open(file, "wb") as stream:
        tomli_w.dump(config, stream)


@click.command()
@click.pass_context
@click.argument("file", type=pathlib.Path)
def pytest_log(ctx: click.Context, file):
    """Add logging to tool.pytest.ini_options table in pyproject.toml"""
    try:
        add_pytest_log(file)
    except FileNotFoundError:
        ctx.exit(f"File not found: {file}")
