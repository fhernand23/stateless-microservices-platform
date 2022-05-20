SRC = $(wildcard **/src/*.py)

.PHONY: deps dev-deps install

deps: dev-deps-app0-admin
	pip install -U -r requirements.txt

dev-deps: deps
	pip install -U -r requirements-dev.txt

lock-requirements:
	pip freeze > requirements.lock

install:
	pip install -U -e ./app0-app1

# deps-app0-admin:
# 	pip install -U app0.admin \
# 	--index https://DEV_PIP_RO:ZrjQS4QnugawsqpmucU2@gitlab.com/api/v4/projects/27627261/packages/pypi/simple \
# 	--extra-index-url https://pypi.org/simple && \
# 	pip install -U app0.platform.auth \
# 	--index https://DEV_PIP_RO:ZrjQS4QnugawsqpmucU2@gitlab.com/api/v4/projects/27627261/packages/pypi/simple \
# 	--extra-index-url https://pypi.org/simple

dev-deps-app0-admin:
	pip install -U -e ../app0-admin/app0-admin
	pip install -U -e ../app0-admin/plugins/platform-auth

api: 
	/bin/bash tools/dev-update-openapi.sh

check-app0-app1:
	/bin/bash app0-app1/build/ci-static-app0-app1.sh

check: check-app0-app1

qa: check
