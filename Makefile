.PHONY: all stop start restart down db django nginx fclean clean inside removeVolumes help logs removeAll stop_container down_container

GREEN  := \033[1;32m
BLUE   := \033[1;34m
YELLOW := \033[1;33m
NC     := \033[0m   

dockerComposeCommand = $(shell docker-compose version >/dev/null 2>&1 && echo docker-compose || echo docker compose)

help:
	@echo -e "$(GREEN)Available Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*
	awk 'BEGIN {FS = ":.*

all:
	@echo -e "$(BLUE)Starting all services...$(NC)"
	$(dockerComposeCommand) up -d --build
	@echo -e "$(GREEN)All services are up and running:$(NC)"
	@echo -e "$(YELLOW)Django:$(NC) http://localhost:8000"
	@echo -e "$(YELLOW)Nginx:$(NC) http://localhost:80"
	@echo -e "$(YELLOW)Portainer:$(NC) http://localhost:9000"

stop:
	@echo -e "$(BLUE)Stopping containers...$(NC)"
	$(dockerComposeCommand) stop

start:
	@echo -e "$(BLUE)Starting containers...$(NC)"
	$(dockerComposeCommand) start

restart:
	@echo -e "$(BLUE)Restarting containers...$(NC)"
	$(dockerComposeCommand) restart

down:
	@echo -e "$(BLUE)Taking down services...$(NC)"
	$(dockerComposeCommand) down

db:
	@echo -e "$(BLUE)Starting database service...$(NC)"
	$(dockerComposeCommand) up -d db

django:
	@echo -e "$(BLUE)Starting Django service...$(NC)"
	$(dockerComposeCommand) up -d django

nginx:
	@echo -e "$(BLUE)Starting Nginx service...$(NC)"
	$(dockerComposeCommand) up -d web

fclean:
	@echo -e "$(BLUE)Removing all containers and images...$(NC)"
	- docker rm -f $$(docker ps -a -q) || true
	- docker rmi -f $$(docker images -q) || true
	- docker network rm $$(docker network ls -q) || true

clean: fclean
	@echo -e "$(BLUE)Removing all volumes and networks...$(NC)"
	- docker volume rm $$(docker volume ls -q) || true
	- docker network rm $$(docker network ls -q) || true

removeVolumes:
	@echo -e "$(BLUE)Removing containers, images, and volumes...$(NC)"
	$(dockerComposeCommand) down -v

inside:
	@echo -e "$(BLUE)Entering container $(YELLOW)$(userinput)$(NC)"
	docker exec -it $(userinput) bash

createapp:
	@echo -e "$(BLUE)Creating Django app $(YELLOW)$(appname)$(NC)"
	$(dockerComposeCommand) exec django python manage.py startapp $(appname)

createsuperuser:
	@echo -e "$(BLUE)Creating Django superuser...$(NC)"
	$(dockerComposeCommand) exec django python manage.py createsuperuser

migrate:
	@echo -e "$(BLUE)Applying migrations...$(NC)"
	$(dockerComposeCommand) exec django python manage.py migrate

makemigrations:
	@echo -e "$(BLUE)Making migrations...$(NC)"
	$(dockerComposeCommand) exec django python manage.py makemigrations

logs:
	@if [ -z "$(service)" ]; then \
		echo -e "$(BLUE)Displaying logs from all services...$(NC)"; \
		$(dockerComposeCommand) logs -f; \
	else \
		echo -e "$(BLUE)Displaying logs from $(YELLOW)$(service)$(NC) service...$(NC)"; \
		$(dockerComposeCommand) logs -f $(service); \
	fi

logs_container:
	@if [ -z "$(container)" ]; then \
		echo -e "$(RED)Error: container name is required.$(NC)"; \
		exit 1; \
	fi
	@echo -e "$(BLUE)Displaying logs from $(YELLOW)$(container)$(NC) container...$(NC)"; \
	while true; do \
		docker logs -f $(container); \
		echo -e "$(RED)Container $(container) stopped. Restarting log display...$(NC)"; \
		sleep 2; \
	done

removeAll:
	@echo -e "$(BLUE)Removing all Docker Compose content...$(NC)"
	$(dockerComposeCommand) down -v --remove-orphans

stop_container:
	@echo -e "$(BLUE)Stopping container $(YELLOW)$(container)$(NC)"
	$(dockerComposeCommand) stop $(container)

down_container:
	@echo -e "$(BLUE)Taking down container $(YELLOW)$(container)$(NC)"
	$(dockerComposeCommand) rm -f $(container)