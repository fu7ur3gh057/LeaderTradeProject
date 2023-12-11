.PHONY: help start stop clean logs

export
DOCKER_PROJECT = ${PROJECT_NAME}

help:
	@echo "Available targets:"
	@echo "help	-	show this help message"
	@echo "start	-	Build  Docker Compose Services in Background"
	@echo "test	-	Build  Docker Compose Services"
	@echo "stop	-	Stop  Docker Compose Services"
	@echo "reset	-	Stop and remove all Docker Compose resources"
	@echo "logs	-	Get last 100 logs"

start:
	docker compose -f docker-compose.yml up -d --build

test:
	docker compose -f docker-compose.yml up --build

stop:
	docker compose -f docker-compose.yml down

reset:
	docker compose -f docker-compose.yml down --volumes  --rmi all

logs:
	docker compose -f docker-compose.yml logs --tail=100