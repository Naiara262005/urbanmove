.DEFAULT_GOAL := help
TF_DEV := terraform -chdir=infra/dev

.PHONY: help install lint format test cov up down logs tf-init tf-apply tf-destroy clean

help: ## Muestra esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-12s %s\n", $$1, $$2}'

install: ## Instala dependencias de desarrollo (usa un venv activo)
	pip install -e ".[dev]"

lint: ## Ruff check + comprobación de formato
	ruff check .
	ruff format --check .

format: ## Aplica ruff format y autofixes
	ruff check --fix .
	ruff format .

test: ## Ejecuta los tests unitarios (sin LocalStack)
	pytest -m "not integration"

cov: ## Tests con cobertura
	pytest -m "not integration" --cov --cov-report=term-missing

up: ## Levanta LocalStack
	docker compose up -d --wait

down: ## Detiene LocalStack y borra volúmenes
	docker compose down -v

logs: ## Sigue los logs de LocalStack
	docker compose logs -f localstack

tf-init: ## terraform init (dev)
	$(TF_DEV) init

tf-apply: ## Despliega la infraestructura dev en LocalStack
	$(TF_DEV) apply -auto-approve

tf-destroy: ## Destruye la infraestructura dev
	$(TF_DEV) destroy -auto-approve

clean: ## Borra cachés locales
	rm -rf .pytest_cache .ruff_cache .coverage htmlcov
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
