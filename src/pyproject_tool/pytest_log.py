import click
import tomli_w
import tomllib


@click.command()
@click.pass_context
@click.option("-f", "--file", help="Path to pyproject.toml", default="pyproject.toml")
def pytest_log(ctx: click.Context, file):
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

    with open(file, "rb") as stream:
        data = tomllib.load(stream)

    tool_table = data.setdefault("tool", {})
    pytest_table = tool_table.setdefault("pytest", {})
    ini_options = pytest_table.setdefault('ini_options', {})
    for key, value in log_defaults.items():
        ini_options.setdefault(key, value)

    with open(file, "wb") as stream:
        tomli_w.dump(data, stream)
