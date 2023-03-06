format:
	pipenv run nbqa black nbs/ examples/
	pipenv run nbqa isort nbs/ examples/

lint:
	pipenv run nbqa mypy nbs/ --ignore-missing-imports --check-untyped-defs

test:
	pipenv run nbdev_test 

export:
	pipenv run nbdev_export 

pipenv-setup:
	pipenv run pipenv-setup sync --pipfile --dev

readme:
	pipenv run nbdev_readme

clean:
	pipenv run nbdev_clean

all: format export test readme clean

docs:
	pipenv run nbdev_docs

bump:
	pipenv run nbdev_bump_version

pypi:
	pipenv run nbdev_pypi

example:
	pipenv run streamlit run examples/example.py

