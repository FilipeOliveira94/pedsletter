# PedsLetter — common development commands
# Requires: GNU make. Node.js and the package manager come in F1-01.

.PHONY: docs-lint help install dev build lint test

# Target not implemented yet: warn and exit with an error, so that no
# script or CI treats a placeholder as a check that passed.
define not_yet
	@echo "make $(1): not implemented yet. It comes in $(2) (see ROADMAP.md)."
	@exit 1
endef

help: ## List the available targets
	@awk 'BEGIN {FS = ":.*##"; printf "Targets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-10s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Install dependencies (placeholder; F1-01)
	$(call not_yet,install,F1-01)

dev: ## Start the Astro dev server (placeholder; F1-01)
	$(call not_yet,dev,F1-01)

build: ## Build the static site (placeholder; F1-01)
	$(call not_yet,build,F1-01)

docs-lint: ## Check Markdown tables (no empty header)
	python3 scripts/check_markdown_tables.py

lint: ## Run lint and type checks (placeholder; F1-01)
	$(call not_yet,lint,F1-01)

test: ## Run the tests (placeholder; F1-01)
	$(call not_yet,test,F1-01)
