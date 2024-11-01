.PHONY: all stop start restart down db django nginx fclean clean inside removeVolumes help logs removeAll stop_container down_container

# Color Codes
GREEN  := \033[1;32m
BLUE   := \033[1;34m
YELLOW := \033[1;33m
NC     := \033[0m    # No Color

# Help Command
help: ## Display this help message
	@echo -e "$(GREEN)Available Commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-15s$(NC)%s\n", $$1, $$2}'

# Build and run the entire Docker Compose environment
all: ## Build and run the entire Docker Compose environment
	@echo -e "$(BLUE)Starting all services...$(NC)"
	docker-compose up -d --build

# Stop running containers
stop: ## Stop running containers
	@echo -e "$(BLUE)Stopping containers...$(NC)"
	docker-compose stop

# Start stopped containers
start: ## Start stopped containers
	@echo -e "$(BLUE)Starting containers...$(NC)"
	docker-compose start

# Restart running containers
restart: ## Restart running containers
	@echo -e "$(BLUE)Restarting containers...$(NC)"
	docker-compose restart

# Bring down the Docker Compose environment
down: ## Bring down the Docker Compose environment
	@echo -e "$(BLUE)Taking down services...$(NC)"
	docker-compose down

# Bring up only the database container
db: ## Bring up only the database container
	@echo -e "$(BLUE)Starting database service...$(NC)"
	docker-compose up -d db

# Bring up only the Django container
django: ## Bring up only the Django container
	@echo -e "$(BLUE)Starting Django service...$(NC)"
	docker-compose up -d django

# Bring up only the Nginx (web) container
nginx: ## Bring up only the Nginx (web) container
	@echo -e "$(BLUE)Starting Nginx service...$(NC)"
	docker-compose up -d web

# Remove all containers and images, but keep volumes
fclean: ## Remove all containers and images, but keep volumes
	@echo -e "$(BLUE)Removing all containers and images...$(NC)"
	docker-compose down 
	docker system prune -af --volumes 

# Clean everything: containers, images, networks, and volumes
purge: fclean ## Clean everything: containers, images, networks, and volumes
	@echo -e "$(BLUE)Removing all volumes and networks...$(NC)"
	- docker volume rm $$(docker volume ls -q) || true
	- docker network rm $$(docker network ls -q) || true

# Remove containers, images, and volumes completely
removeVolumes: ## Remove containers, images, and volumes completely
	@echo -e "$(BLUE)Removing containers, images, and volumes...$(NC)"
	docker-compose down -v

# Enter a running container interactively
inside: ## Enter a running container interactively (Usage: make inside userinput=container_name)
	@echo -e "$(BLUE)Entering container $(YELLOW)$(userinput)$(NC)"
	docker exec -it $(userinput) bash

# Create a new Django app
createapp: ## Create a new Django app (Usage: make createapp appname=your_app_name)
	@echo -e "$(BLUE)Creating Django app $(YELLOW)$(appname)$(NC)"
	docker-compose exec django python manage.py startapp $(appname)

# Create a Django superuser
createsuperuser: ## Create a Django superuser
	@echo -e "$(BLUE)Creating Django superuser...$(NC)"
	docker-compose exec django python manage.py createsuperuser

# Apply migrations
migrate: ## Apply database migrations
	@echo -e "$(BLUE)Applying migrations...$(NC)"
	docker-compose exec django python manage.py migrate

# Make migrations
makemigrations: ## Create new migrations based on model changes
	@echo -e "$(BLUE)Making migrations...$(NC)"
	docker-compose exec django python manage.py makemigrations

# View logs of containers in real time
logs: ## View logs of containers in real time (Usage: make logs [service=service_name])
	@if [ -z "$(service)" ]; then \
		echo -e "$(BLUE)Displaying logs from all services...$(NC)"; \
		docker-compose logs -f; \
	else \
		echo -e "$(BLUE)Displaying logs from $(YELLOW)$(service)$(NC) service...$(NC)"; \
		docker-compose logs -f $(service); \
	fi

# Remove all Docker Compose content related to this project
removeAll: ## Remove all Docker Compose content related to this project
	@echo -e "$(BLUE)Removing all Docker Compose content...$(NC)"
	docker-compose down -v --remove-orphans

# Stop a specific container
stop_container: ## Stop a specific container (Usage: make stop_container container=container_name)
	@echo -e "$(BLUE)Stopping container $(YELLOW)$(container)$(NC)"
	docker-compose stop $(container)

# Bring down a specific container
down_container: ## Bring down a specific container (Usage: make down_container container=container_name)
	@echo -e "$(BLUE)Taking down container $(YELLOW)$(container)$(NC)"
	docker-compose rm -f $(container)