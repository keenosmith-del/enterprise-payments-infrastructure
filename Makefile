SHELL := /bin/bash
COMPOSE := docker compose --env-file .local/epi.env
.PHONY: bootstrap up down migrate seed test lint typecheck build verify status logs
bootstrap:
	python3 scripts/m01/create_env.py
up: bootstrap
	$(COMPOSE) up -d --build --wait
down:
	$(COMPOSE) down
migrate:
	$(COMPOSE) run --rm database-setup
seed: migrate
status:
	$(COMPOSE) ps
logs:
	$(COMPOSE) logs --tail=100
build: bootstrap
	$(COMPOSE) build
lint:
	ruff check packages scripts/m01 tests/unit
typecheck:
	mypy packages/epi_foundation tests/unit
test:
	python -m pytest tests/unit -q
verify: lint typecheck test
	npm run typecheck
	npm run build
