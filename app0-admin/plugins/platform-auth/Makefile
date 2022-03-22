SRC = $(wildcard src/*.py)

.PHONY: check test install clean

test:
	export PYTHONPATH=src && \
		pytest --cov-fail-under=90 --cov-report=term --cov=src  ./test/unit

install:
	pip install -e .

deps:
	pip install -r requirements.txt

dev-deps:
	pip install -r requirements.txt && \
	pip install -r requirements-dev.txt

lock-requirements:
	rm -i requirements.lock
	pip freeze > requirements.lock

dist: clean test
	python setup.py sdist bdist_wheel

pypi: dist
	twine upload --repository pypi dist/*

clean:
	rm -rf dist

check: pylint flake8  mypy

mypy:
	python -m mypy ./src/app0/platform/auth ./test/unit/.

flake8:
	python -m flake8 --max-line-length=120 ./src/app0/platform/auth ./test/unit/.

pylint:
	python -m pylint ./src/app0/platform/auth
