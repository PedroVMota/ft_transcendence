.PHONY: all stop start restart down Database Django Nginx fclean clean inside
all:
	docker-compose up --build

stop:
	docker-compose stop

start:
	docker-compose start

restart:
	docker-compose restart

down:
	docker-compose down

Database:
	docker-compose up db 

Django:
	docker-compose up django

Nginx:
	docker-compose up web

fclean: down
	- docker stop $$(docker ps -a -q)
	- docker rm $$(docker ps -a -q)
	- docker rmi $$(docker images -q)
	- docker volume rm $$(docker volume ls -q)
	- docker network rm $$(docker network ls -q)

clean: fclean
	- docker rmi $$(docker images -q)
	- docker volume rm $$(docker volume ls -q)
	- docker network rm $$(docker network ls -q)


# make inside userinput=Nginx
inside:
	docker exec -it $(userinput) bash