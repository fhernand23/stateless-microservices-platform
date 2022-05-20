SRC = $(wildcard **/src/*.py)

.PHONY: deps dev-deps install

deps:
	pip install -U -r requirements.txt

dev-deps: deps
	pip install -U -r requirements-dev.txt

lock-requirements:
	pip freeze > requirements.lock

install:
	pip install -U -e ./app0-admin && \
	pip install -U -e ./plugins/platform-auth

check-app0-admin:
	/bin/bash app0-admin/build/ci-static-app0-admin.sh

check-platform-auth:
	/bin/bash plugins/platform-auth/build/ci-static-plugins.sh

check: check-app0-admin check-platform-auth

qa: check

api: 
	/bin/bash dev-update-openapi.sh
