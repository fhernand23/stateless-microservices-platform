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
	/bin/bash tools/dev-update-openapi.sh

dist-app0-admin:
	pip install wheel && \
	cd app0-admin && \
	rm -rf dist && \
	python setup.py sdist bdist_wheel

dist-plugin-auth:
	pip install wheel && \
	cd plugins/platform-auth/ && \
	rm -rf dist && \
	python setup.py sdist bdist_wheel

build-docker-api:
	$(eval ENGINE_VERSION := $(shell cat requirements.lock | grep hopeit.engine |  sed s/'hopeit.engine=='//))
	$(eval CA_BASE_VERSION := $(shell python app0-admin/config/version.py CA_BASE_VERSION))
	docker build --progress plain --build-arg ENGINE_VERSION=$(ENGINE_VERSION) \
	--tag app0-admin \
	--tag app0-admin:$(CA_BASE_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/app0-admin:$(CA_BASE_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/app0-admin .

build-docker-app0-visualizer:
	$(eval ENGINE_VERSION := $(shell cat requirements.lock | grep hopeit.engine |  sed s/'hopeit.engine=='//))
	$(eval CA_BASE_VERSION := $(shell python app0-admin/config/version.py CA_BASE_VERSION))
	cd docker && cd apps-visualizer && docker build --progress plain --build-arg ENGINE_VERSION=$(ENGINE_VERSION) \
	--tag app0-visualizer \
	--tag app0-visualizer:$(CA_BASE_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/apps-visualizer:$(CA_BASE_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/apps-visualizer .
	
build-docker-ui:
	$(eval UI_VERSION := $(shell grep '"version"' app0-admin-ui/package.json | cut -d '"' -f 4 | head -n 1))
	cd app0-admin-ui && docker build --progress plain \
	--tag app0-admin-ui \
	--tag app0-admin-ui:$(UI_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/app0-admin-ui:$(UI_VERSION) \
	--tag registry.gitlab.com/newken/app0-admin/app0-admin-ui .

publish-docker-api:
	$(eval CA_BASE_VERSION := $(shell python app0-admin/config/version.py CA_BASE_VERSION))
	docker push registry.gitlab.com/newken/app0-admin/app0-admin:$(CA_BASE_VERSION) && \
	docker push registry.gitlab.com/newken/app0-admin/app0-admin

publish-docker-ui:
	$(eval UI_VERSION := $(shell grep '"version"' app0-admin-ui/package.json | cut -d '"' -f 4 | head -n 1))
	docker push registry.gitlab.com/newken/app0-admin/app0-admin-ui:$(UI_VERSION) && \
	docker push registry.gitlab.com/newken/app0-admin/app0-admin-ui

publish-docker-apps-visualizer:
	$(eval CA_BASE_VERSION := $(shell python app0-admin/config/version.py CA_BASE_VERSION))
	docker push registry.gitlab.com/newken/app0-admin/apps-visualizer:$(CA_BASE_VERSION) && \
	docker push registry.gitlab.com/newken/app0-admin/apps-visualizer