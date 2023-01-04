format:
	pipenv run nbqa black nbs/
	pipenv run nbqa isort nbs/

lint:
	pipenv run nbqa mypy nbs/

test:
	pipenv run nbdev_test 

export:
	pipenv run nbdev_export 

pipenv-setup:
	pipenv run pipenv-setup sync --pipfile --dev

readme:
	pipenv run nbdev_readme

all: format lint test export readme


