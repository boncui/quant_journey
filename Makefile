SHELL := /bin/bash
CORE  := quant_core
CC    := command_center

.PHONY: help setup run test test-core test-all lint fmt relock relock-all list \
        cc cc-setup cc-seed cc-api cc-test cc-build cc-dev

help:
	@echo "quant_journey — make targets"
	@echo "  make setup [N=1]     sync quant_core (+ project N if given)"
	@echo "  make run N=1 [ARGS='--tickers SPY KO']   run project N"
	@echo "  make test N=1        test project N        (omit N => test quant_core)"
	@echo "  make test-all        test quant_core + every project"
	@echo "  make lint | fmt      ruff check / format the whole repo"
	@echo "  make relock N=1 | relock-all   re-lock after quant_core deps change"
	@echo "  make list            list existing projects"
	@echo "  --- command_center (research terminal) ---"
	@echo "  make cc-setup        sync backend (uv) + install frontend (npm)"
	@echo "  make cc              seed + build + serve the whole terminal at :8000"
	@echo "  make cc-dev          FastAPI :8000 + Vite :5173 (hot reload)"
	@echo "  make cc-seed | cc-api | cc-test | cc-build"

# Resolve a zero-padded project dir from N (1 -> 001_*). Sets shell var $$dir.
define _resolve
dir=$$(ls -d $$(printf '%03d' $(N))_*/ 2>/dev/null | head -n1); \
test -n "$$dir" || { echo "No project directory for N=$(N)."; exit 1; }
endef

setup:
	uv sync --directory $(CORE) --extra yfinance
	@if [ -n "$(N)" ]; then $(_resolve); echo ">> syncing $$dir"; uv sync --directory "$$dir"; fi

run:
	@test -n "$(N)" || { echo "usage: make run N=<num> [ARGS='...']"; exit 2; }
	@$(_resolve); echo ">> $$dir"; uv run --directory "$$dir" python main.py $(ARGS)

test:
	@if [ -z "$(N)" ]; then $(MAKE) test-core; else \
	  $(_resolve); echo ">> testing $$dir"; uv run --directory "$$dir" pytest; fi

test-core:
	uv run --directory $(CORE) pytest

test-all: test-core
	@for dir in [0-9][0-9][0-9]_*/; do \
	  [ -d "$$dir" ] || continue; echo ">> testing $$dir"; \
	  uv run --directory "$$dir" pytest || exit 1; done

# Lint/format the whole repo using quant_core's env (which carries ruff); root ruff.toml applies.
lint:
	uv run --project $(CORE) ruff check .

fmt:
	uv run --project $(CORE) ruff format .

# Re-lock after quant_core's dependencies change (editable source changes need no relock).
relock:
	@test -n "$(N)" || { echo "usage: make relock N=<num>"; exit 2; }
	@$(_resolve); echo ">> relocking $$dir"; uv lock --directory "$$dir" --upgrade-package quant-core

relock-all:
	uv lock --directory $(CORE)
	@for dir in [0-9][0-9][0-9]_*/; do \
	  [ -d "$$dir" ] || continue; echo ">> relocking $$dir"; \
	  uv lock --directory "$$dir" --upgrade-package quant-core; done
	uv lock --directory $(CC)/backend --upgrade-package quant-core

# --- command_center: research terminal (FastAPI backend + React frontend) ---
cc-setup:
	uv sync --directory $(CC)/backend
	cd $(CC)/frontend && npm install

cc-seed:
	uv run --directory $(CC)/backend python -m app.seed

# Dump OpenAPI from the app (offline) and regenerate the committed TS types from it.
cc-api:
	uv run --directory $(CC)/backend python -m app.openapi_dump
	cd $(CC)/frontend && npm run api:gen

cc-test:
	uv run --directory $(CC)/backend pytest
	cd $(CC)/frontend && npm run typecheck && npm test

cc-build:
	cd $(CC)/frontend && npm run build

# Dev: FastAPI + Vite together (Vite proxies /api -> :8000). Ctrl-C stops the foreground Vite.
cc-dev:
	@echo ">> FastAPI :8000 (background) + Vite :5173"
	uv run --directory $(CC)/backend uvicorn app.main:app --reload --port 8000 & \
	cd $(CC)/frontend && npm run dev

# Daily driver: seed synthetic data if needed, build the SPA, and serve everything at :8000.
cc:
	@$(MAKE) cc-seed
	@$(MAKE) cc-build
	@echo ">> command_center on http://localhost:8000"
	CC_FRONTEND_DIST=../frontend/dist uv run --directory $(CC)/backend uvicorn app.main:app --port 8000

list:
	@echo "Projects on disk:"; ls -d [0-9][0-9][0-9]_*/ 2>/dev/null || echo "  (none yet)"
	@echo "Full 100-project index: see README.md"
