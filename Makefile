SHELL := /bin/bash
COMPOSE := docker compose --env-file .local/epi.env
PYTHON := .venv/bin/python
.PHONY: credentials bootstrap up down migrate seed test lint typecheck build verify status logs
credentials:
	python3 scripts/m01/create_env.py
bootstrap: credentials
	python3 -c 'import sys; assert sys.version_info >= (3,14), "Python 3.14 or newer is required"'
	node -e 'if (+process.versions.node.split(".")[0] < 24) throw Error("Node 24 or newer is required")'
	python3 -m venv .venv
	$(PYTHON) -m pip install --require-hashes -r requirements.lock
	npm ci
	npx playwright install chromium
	python3 -m venv .venv-security
	.venv-security/bin/pip install --require-hashes -r security-requirements.lock
up: credentials
	$(COMPOSE) up -d --build --wait
down:
	$(COMPOSE) down
migrate: credentials
	$(COMPOSE) run --rm database-setup
seed: migrate
status:
	$(COMPOSE) ps
logs:
	$(COMPOSE) logs --tail=100
build: credentials
	$(COMPOSE) build
lint:
	.venv/bin/ruff check packages scripts/m01 tests/unit services

typecheck:
	.venv/bin/mypy packages/epi_foundation tests/unit

test:
	$(PYTHON) -m pytest tests/unit -q

verify:
	bash scripts/m01/verify.sh
