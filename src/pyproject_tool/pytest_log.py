
import click
import tomli_w
import tomllib

DEFAULTS = {
    'log_cli': True,
    'log_cli_level': "DEBUG",
    'log_cli_format': '%(levelname)s:%(name)s:%(message)s',
    'log_cli_date_format': '%Y-%m-%d %H:%M:%S',
    'log_file': 'pytest.log',
    'log_file_level': 'DEBUG',
    'log_file_format': '%(levelname)s:%(name)s:%(message)s',
    'log_file_date_format': '%Y-%m-%d %H:%M:%S',
}


@click.command()
@click.pass_context
def pytest_log(ctx: click.Context):
    with open("pyproject.toml", "rb") as stream:
        data = tomllib.load(stream)

    pytest_options = data.setdefault('tool.pytest.ini_options', {})
    for key, value in DEFAULTS.items():
        pytest_options.setdefault(key, value)
        
    with open("/tmp/pyproject.toml", "wb") as stream:
        tomli_w.dump(data, stream)
