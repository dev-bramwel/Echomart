.PHONY: help build snapshot up start rebuild down stop restart logs migrate makemigrations shell test test-backend lint lint-backend lint-frontend format format-backend format-frontend format-check format-check-backend format-check-frontend frontend-build clean rollback

COMPOSE := docker compose
BACKEND_IMAGE := echomart-backend:latest
FRONTEND_IMAGE := echomart-frontend:latest
DATABASE_IMAGE := echomart-db:latest

help:
	@echo "Echomart development shortcuts:"
	@echo "  make build          Build all Docker images"
	@echo "  make up             Build and start the stack"
	@echo "  make start          Start existing stopped containers"
	@echo "  make rebuild        Snapshot images, rebuild, and restart"
	@echo "  make rollback       Restore images from the last rebuild snapshot"
	@echo "  make stop           Stop containers without removing them"
	@echo "  make down           Stop and remove containers"
	@echo "  make logs           Follow service logs"
	@echo "  make migrate        Apply Django migrations"
	@echo "  make makemigrations Create Django migrations"
	@echo "  make shell          Open a Django shell"
	@echo "  make test           Run backend tests"
	@echo "  make lint           Run backend and frontend linting"
	@echo "  make format         Format backend and frontend code"
	@echo "  make format-check   Check backend formatting and frontend lint rules"
	@echo "  make clean          Remove containers and volumes"

snapshot:
	@if docker image inspect $(BACKEND_IMAGE) >/dev/null 2>&1; then docker image tag $(BACKEND_IMAGE) $(BACKEND_IMAGE)-rollback; fi
	@if docker image inspect $(FRONTEND_IMAGE) >/dev/null 2>&1; then docker image tag $(FRONTEND_IMAGE) $(FRONTEND_IMAGE)-rollback; fi
	@if docker image inspect $(DATABASE_IMAGE) >/dev/null 2>&1; then docker image tag $(DATABASE_IMAGE) $(DATABASE_IMAGE)-rollback; fi

build:
	$(COMPOSE) build

up:
	$(COMPOSE) up -d --build --force-recreate

start:
	$(COMPOSE) start

rebuild: snapshot
	$(COMPOSE) build --no-cache
	$(COMPOSE) up -d --force-recreate

rollback:
	@if ! docker image inspect $(BACKEND_IMAGE)-rollback >/dev/null 2>&1 || ! docker image inspect $(FRONTEND_IMAGE)-rollback >/dev/null 2>&1 || ! docker image inspect $(DATABASE_IMAGE)-rollback >/dev/null 2>&1; then echo "No complete rollback snapshot exists."; exit 1; fi
	$(COMPOSE) down --remove-orphans
	docker image tag $(BACKEND_IMAGE)-rollback $(BACKEND_IMAGE)
	docker image tag $(FRONTEND_IMAGE)-rollback $(FRONTEND_IMAGE)
	docker image tag $(DATABASE_IMAGE)-rollback $(DATABASE_IMAGE)
	$(COMPOSE) up -d

down:
	$(COMPOSE) down --remove-orphans

stop:
	$(COMPOSE) stop

restart:
	$(COMPOSE) restart

logs:
	$(COMPOSE) logs -f

migrate:
	$(COMPOSE) exec backend python manage.py migrate

makemigrations:
	$(COMPOSE) exec backend python manage.py makemigrations

shell:
	$(COMPOSE) exec backend python manage.py shell

test: test-backend

test-backend:
	$(COMPOSE) exec backend python manage.py test

lint: lint-backend lint-frontend

lint-backend:
	$(COMPOSE) run --rm backend python manage.py check
	$(COMPOSE) run --rm backend ruff check .

lint-frontend:
	$(COMPOSE) run --rm frontend npm run lint

format: format-backend format-frontend

format-backend:
	$(COMPOSE) run --rm backend black .

format-frontend:
	$(COMPOSE) run --rm frontend npm run lint -- --fix

format-check: format-check-backend format-check-frontend

format-check-backend:
	$(COMPOSE) run --rm backend black --check .
	$(COMPOSE) run --rm backend ruff check .

format-check-frontend:
	$(COMPOSE) run --rm frontend npm run lint

frontend-build:
	$(COMPOSE) build frontend

clean:
	$(COMPOSE) down --volumes --remove-orphans
