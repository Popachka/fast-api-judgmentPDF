# Makefile

.PHONY: build build-prod up up-prod down down-prod logs logs-prod

build:
	docker-compose build

build-prod:
	docker-compose -f docker-compose.prod.yaml build

up:
	docker-compose up -d

up-prod:
	docker-compose  -f docker-compose.prod.yaml up -d

down:
	docker-compose down

down-prod:
	docker-compose -f docker-compose.prod.yaml down

logs:
	docker-compose logs -f

logs-prod:
	docker-compose -f docker-compose.prod.yaml logs -f

ps:
	docker-compose ps

ps-prod:
	docker-compose  -f docker-compose.prod.yaml ps

migrate:
	docker-compose run app alembic upgrade head

migrate-prod:
	docker-compose  f docker-compose.prod.yaml run app alembic upgrade head
