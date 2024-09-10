.PHONY: all stop start restart down Database Django Nginx fclean clean inside removeVolumes

# Build and run the entire Docker Compose environment
all:
	docker-compose up --build 

# Stop running containers
stop:
	docker-compose stop

# Start stopped containers
start:
	docker-compose start 

# Restart running containers
restart: 
	docker-compose restart 

# Bring down the Docker Compose environment
down:
	docker-compose down

# Bring up only the database container
Database:
	docker-compose up db

# Bring up only the Django container
Django:
	docker-compose up django

# Bring up only the Nginx (web) container
Nginx:
	docker-compose up web

# Remove all containers and images, but keep volumes
fclean:
	@echo "Removing all containers and images..."
	- docker rm -f $$(docker ps -a -q) || true
	- docker rmi -f $$(docker images -q) || true
	- docker network rm $$(docker network ls -q) || true

# Clean everything: containers, images, networks, and volumes
clean: fclean
	@echo "Removing all volumes and networks..."
	- docker volume rm $$(docker volume ls -q) || true
	- docker network rm $$(docker network ls -q) || true

# Remove containers, images, and volumes completely
removeVolumes:
	docker-compose down -v

# Enter a running container interactively using the 'userinput' variable
# Example: make inside userinput=web
inside:
	docker exec -it $(userinput) bash
