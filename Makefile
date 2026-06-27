# Convenience targets for local development. Requires Docker + Docker Compose.

.PHONY: up down build logs test api-shell migrate makemigration downgrade

up:           ## Start the full stack (db, redis, api, web)
	docker compose up

build:        ## Rebuild all images
	docker compose build

down:         ## Stop and remove containers
	docker compose down

logs:         ## Tail logs for all services
	docker compose logs -f

test:         ## Run backend tests inside the api container
	docker compose run --rm api pytest

migrate:      ## Apply DB migrations (alembic upgrade head)
	docker compose run --rm api alembic upgrade head

makemigration: ## Autogenerate a migration: make makemigration msg="add x"
	docker compose run --rm api alembic revision --autogenerate -m "$(msg)"

downgrade:    ## Roll back the last migration
	docker compose run --rm api alembic downgrade -1

api-shell:    ## Open a shell in the api container
	docker compose run --rm api bash
