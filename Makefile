format:
	uv run nbqa black nbs/ examples/
	uv run nbqa isort nbs/ examples/

test:
	uv run nbdev_test

export:
	uv run nbdev_export

setup:
	uv sync --dev
	uv run pip install -e .

readme:
	uv run nbdev_readme

clean:
	uv run nbdev_clean

all: format export test readme clean

docs:
	uv run nbdev_docs

bump:
	uv run nbdev_bump_version

pypi:
	uv run nbdev_pypi

example: setup
	uv run streamlit run examples/example.py --server.runOnSave true

