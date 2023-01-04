format:
	pipenv run nbqa black nbs/
	pipenv run nbqa isort nbs/

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
	nbdev_clean

all: format test export readme clean


