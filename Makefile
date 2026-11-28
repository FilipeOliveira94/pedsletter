# PedsLetter — common development commands
# Requires: GNU make, Node.js (version in .nvmrc) and npm.

.PHONY: docs-lint help install dev build lint test

# Target not implemented yet: warn and exit with an error, so that no
# script or CI treats a placeholder as a check that passed.
define not_yet
	@echo "make $(1): not implemented yet. It comes in $(2) (see ROADMAP.md)."
	@exit 1
endef

help: ## List the available targets
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-10s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install dependencies from the lockfile
	npm ci

dev: ## Start the Astro dev server
	npm run dev

build: ## Build the static site into dist/
	npm run build

docs-lint: ## Check Markdown tables (no empty header)
	python3 scripts/check_markdown_tables.py

lint: ## Type-check the project (astro check; a type error fails)
	npm run check

test: ## Run the tests (placeholder; the first test comes in F1-03)
	$(call not_yet,test,F1-03)
