import pathlib

import pytest

from pyproject_tool import add_pytest_log, update_config


@pytest.mark.parametrize(
    ["config", "expected"],
    [
        pytest.param(
            {},
            {
                "tool": {
                    "pytest": {
                        "ini_options": {
                            "log_cli": True,
                            "log_cli_level": "DEBUG",
                            "log_cli_format": "%(levelname)-8s | %(name)s:%(message)s",
                            "log_cli_date_format": "%Y-%m-%d %H:%M:%S",
                            "log_file": "pytest.log",
                            "log_file_level": "DEBUG",
                            "log_file_format": "%(levelname)-8s | %(name)s:%(message)s",
                            "log_file_date_format": "%Y-%m-%d %H:%M:%S",
                        }
                    }
                }
            },
            id="empty config",
        ),
        pytest.param(
            {"tool": {"pytest": {"ini_options": {"log_cli": False}}}},
            {
                "tool": {
                    "pytest": {
                        "ini_options": {
                            "log_cli": False,
                            "log_cli_level": "DEBUG",
                            "log_cli_format": "%(levelname)-8s | %(name)s:%(message)s",
                            "log_cli_date_format": "%Y-%m-%d %H:%M:%S",
                            "log_file": "pytest.log",
                            "log_file_level": "DEBUG",
                            "log_file_format": "%(levelname)-8s | %(name)s:%(message)s",
                            "log_file_date_format": "%Y-%m-%d %H:%M:%S",
                        }
                    }
                }
            },
            id="no overwrite",
        ),
    ],
)
def test_add_pytest_log(config, expected):
    update_config(config)
    assert config == expected


CONFIG1 = """
[project]
name = "my-project"
"""

EXPECTED1 = """[project]
name = "my-project"

[tool.pytest.ini_options]
log_cli = true
log_cli_level = "DEBUG"
log_cli_format = "%(levelname)-8s | %(name)s:%(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
log_file = "pytest.log"
log_file_level = "DEBUG"
log_file_format = "%(levelname)-8s | %(name)s:%(message)s"
log_file_date_format = "%Y-%m-%d %H:%M:%S"
"""

CONFIG2 = """
[project]
name = "my-project"

[tool.pytest.ini_options]
log_cli = false
log_cli_level = "INFO"
"""

EXPECTED2 = """[project]
name = "my-project"

[tool.pytest.ini_options]
log_cli = false
log_cli_level = "INFO"
log_cli_format = "%(levelname)-8s | %(name)s:%(message)s"
log_cli_date_format = "%Y-%m-%d %H:%M:%S"
log_file = "pytest.log"
log_file_level = "DEBUG"
log_file_format = "%(levelname)-8s | %(name)s:%(message)s"
log_file_date_format = "%Y-%m-%d %H:%M:%S"
"""


@pytest.mark.parametrize(
    ["content", "expected"],
    [
        pytest.param(CONFIG1, EXPECTED1, id="empty config"),
        pytest.param(CONFIG2, EXPECTED2, id="no overwrite"),
    ],
)
def test_modify_file(content: str, expected: str, tmp_path: pathlib.Path):
    file = tmp_path / "pyproject.toml"

    file.write_text(content)
    add_pytest_log(file)

    new_content = file.read_text()
    assert new_content == expected


def test_modify_non_existent_file(tmp_path):
    file = tmp_path / "pyproject.toml"
    with pytest.raises(FileNotFoundError):
        add_pytest_log(file)
