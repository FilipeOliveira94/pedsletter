# PedsLetter — common development commands
# Requires: GNU make, Node.js (version in .nvmrc) and npm.

.PHONY: authorship docs-lint help hooks install dev build lint site-check test

# No Astro telemetry, locally or in CI (AGENTS.md §8).
export ASTRO_TELEMETRY_DISABLED := 1

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

site-check: ## Walk dist/ for noindex, notices, scripts, sitemap, robots.txt and _headers (F1-03; needs make build)
	python3 scripts/site_check.py dist

test: ## Run the unit tests
	python3 -m unittest discover -s tests

authorship: ## Check tracked files, dist/ and the PR text for authorship (F1-06; needs make build and AUTHORSHIP_BLOCKED_NAMES)
	python3 scripts/authorship_check.py --repo --html dist --text-env PR_TITLE --text-env PR_BODY

hooks: ## Turn on the repository's git hooks (pre-commit authorship check)
	git config core.hooksPath scripts/hooks
