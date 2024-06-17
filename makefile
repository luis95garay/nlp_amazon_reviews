SHELL := /bin/bash
# Just colors
RED=\033[0;31m
GREEN=\033[0;32m
NC=\033[0m

# Network name (default: asistente_api)
NETWORK?=sentiment_classification_net
export NETWORK_NAME=$(NETWORK)
NETWORKS=$(shell docker network ls --filter name=^${NETWORK_NAME} --format="{{ .Name }}")

# Compose Files
BASE_FILE=docker/docker-compose.yml
DEV_FILE=docker/docker-compose.dev.yml
PROD_FILE=docker/docker-compose.prod.yml
PROD_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(PROD_FILE)
DEV_COMPOSE_CMD=docker-compose -f $(CURDIR)/$(BASE_FILE) -f $(CURDIR)/$(DEV_FILE)

create_network:
	@if [ -z $(NETWORKS) ]; then \
		printf "${GREEN}Creating network '$(NETWORK_NAME)'${NC}"; \
		docker network create $(NETWORK_NAME); \
	fi;

build: create_network
	$(PROD_COMPOSE_CMD) build

run:
	$(PROD_COMPOSE_CMD) up -d

build_dev: create_network
	$(DEV_COMPOSE_CMD) build

run_dev:
	$(DEV_COMPOSE_CMD) up -d

run_api: run
	$(PROD_COMPOSE_CMD) exec api /start-reload.sh

stop:
	$(PROD_COMPOSE_CMD) down --remove-orphans

stop_dev:
	$(DEV_COMPOSE_CMD) down --remove-orphans

install:
	pip install poetry==1.7.1 &&\
 	poetry install --only dev --no-root
	
lint:
	poetry run python -m flake8 --ignore=E501,E402,F401 --exclude .venv

scan_files:
	poetry run python -m bandit -r . -lll  --exclude .venv

test:
	poetry run python -m pytest .