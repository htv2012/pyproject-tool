.PHONY: \
	all \
	clean \
	install \
	lab \
	lint \
	py \
	rename \
	run \
	test \

sandbox:
	cp pyproject.toml sample.toml
	uv run pyproject-tool pytest-log --file=sample.toml
	bat sample.toml
	rm sample.toml
### Default target(s)
all: test run

### Clean up generated files
clean:
	uv clean
	rm -fr .ruff_cache .venv

### Install this tool locally
install:
	uv tool install --upgrade .

### Run Jupyter lab
lab:
	JUPYTER_CONFIG_DIR=etc uv run jupyter lab --notebook-dir=etc/notebooks

### Perform static analysis
lint:
	uv tool run ruff check --select I --fix .
	uv tool run ruff format .
	uv tool run ruff check . --fix

### Open a Python shell
py:
	PYTHONSTARTUP= uv run ipython --profile-dir=./etc/ipython

### Rename the project
rename:
	uv run etc/set_project_name.py

### Run the project
run: lint
	PYTHONBREAKPOINT="pudb.set_trace" uv run pyproject-tool
	PYTHONBREAKPOINT="pudb.set_trace" uv run pyproject-tool --version

### Run unit tests
test: lint
	PYTHONBREAKPOINT="pudb.set_trace" uv run pytest -vv

