import pytest

from pyproject_tool.pytest_log import add_pytest_log


@pytest.mark.parametrize(
    ["pytest_ini", "expected"],
    [
        pytest.param(
            {},
            {
                "log_cli": True,
                "log_cli_level": "DEBUG",
                "log_cli_format": "%(levelname)-8s | %(name)s:%(message)s",
                "log_cli_date_format": "%Y-%m-%d %H:%M:%S",
                "log_file": "pytest.log",
                "log_file_level": "DEBUG",
                "log_file_format": "%(levelname)-8s | %(name)s:%(message)s",
                "log_file_date_format": "%Y-%m-%d %H:%M:%S",
            },
            id="empty config",
        ),
        pytest.param(
            {"log_cli": False},
            {
                "log_cli": False,
                "log_cli_level": "DEBUG",
                "log_cli_format": "%(levelname)-8s | %(name)s:%(message)s",
                "log_cli_date_format": "%Y-%m-%d %H:%M:%S",
                "log_file": "pytest.log",
                "log_file_level": "DEBUG",
                "log_file_format": "%(levelname)-8s | %(name)s:%(message)s",
                "log_file_date_format": "%Y-%m-%d %H:%M:%S",
            },
            id="no overwrite",
        ),
    ],
)
def test_add_pytest_log(pytest_ini, expected):
    add_pytest_log(pytest_ini)
    assert pytest_ini == expected
