# PedsLetter — comandos comuns de desenvolvimento
# Requer: GNU make. Node.js e o gerenciador de pacotes entram em F1-01.

.PHONY: help install dev build lint test

# Alvo ainda sem implementação: avisa e sai com erro, para que nenhum
# script ou CI trate um marcador como verificação que passou.
define not_yet
	@echo "make $(1): ainda não implementado. Entra em $(2) (ver ROADMAP.md)."
	@exit 1
endef

help: ## Lista os alvos disponíveis
	@awk 'BEGIN {FS = ":.*##"; printf "Alvos:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  %-10s %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: ## Instala as dependências (marcador; F1-01)
	$(call not_yet,install,F1-01)

dev: ## Sobe o servidor de desenvolvimento do Astro (marcador; F1-01)
	$(call not_yet,dev,F1-01)

build: ## Gera o site estático (marcador; F1-01)
	$(call not_yet,build,F1-01)

lint: ## Roda lint e checagem de tipos (marcador; F1-01)
	$(call not_yet,lint,F1-01)

test: ## Roda os testes (marcador; F1-01)
	$(call not_yet,test,F1-01)
