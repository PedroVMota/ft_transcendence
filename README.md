# Transcendence Project README

## Table of Contents
1. [Modules](#Modules)
2. [Introduction](#introduction)
3. [Key Components of Django](#key-components-of-django)
   - [Models](#models)
   - [URLs](#urls)
   - [Views](#views)
   - [Templates](#templates)
   - [Middleware](#middleware)
   - [Forms](#forms)
   - [Static Files](#static-files)
4. [Basic Django Commands](#basic-django-commands)
5. [Migrations in Django](#migrations-in-django)
6. [Transcendence Project Structure](#transcendence-project-structure)
7. [Docker Concepts for the Project](#docker-concepts-for-the-project)
8. [Setting Up and Running the Project](#setting-up-and-running-the-project)
9. [Deployment](#deployment)
10. [Conclusion](#conclusion)
11. [Date Changes](#changes)

---
## Modules
Here’s an improved table that includes details on each module's relevant aspects, highlighting whether each module is mandatory or optional according to the project structure.

| **Module**               | **Mandatory** | **Type** | **Key Aspects**                                                                                       |
|--------------------------|---------------|----------|-------------------------------------------------------------------------------------------------------|
| **Web**                  | No            | Major    | Backend with Django framework, Ethereum blockchain for score storage, PostgreSQL integration          |
|                          | No            | Minor    | Frontend toolkit with Bootstrap, enhanced database integration                                        |
| **User Management**      | Yes           | Major    | Secure authentication (OAuth 2.0 with 42 API), friend system, profile customization                   |
| **Gameplay**             | Yes           | Major    | Multiplayer gameplay with remote players, tournament matchmaking                                      |
|                          | No            | Minor    | Customization options (power-ups, maps), live chat with interaction features                          |
| **AI-Algo**              | No            | Major    | AI opponent without A* algorithm, simulates player behavior                                           |
|                          | No            | Minor    | User and game statistics dashboards, user insights                                                    |
| **Cybersecurity**        | Yes           | Major    | WAF/ModSecurity, HashiCorp Vault for secure secrets management                                        |
|                          | No            | Minor    | GDPR compliance (user anonymization, data management), account deletion                               |
|                          | Yes           | Major    | Two-Factor Authentication (2FA) and JWT for secure access                                             |
| **DevOps**               | No            | Major    | Log management with ELK stack, microservices architecture for scalability                             |
|                          | No            | Minor    | System monitoring with Prometheus and Grafana, alerting for performance issues                        |
| **Gaming**               | No            | Major    | Addition of new games with user history and matchmaking                                               |
|                          | No            | Minor    | Game customization across platform (maps, difficulty levels, etc.)                                    |
| **Graphics**             | No            | Major    | Advanced 3D graphics with ThreeJS/WebGL for immersive gameplay                                        |
| **Accessibility**        | No            | Minor    | Support for multiple devices, multi-language options, visually impaired accessibility, SSR integration |
| **Server-Side Pong**     | Yes           | Major    | Server-side Pong with API, playable via CLI and web interface                                         |
|                          | No            | Major    | CLI interaction with web players through API integration                                              |

This table provides a clearer breakdown of each module’s features and highlights the mandatory elements required to achieve a complete project according to the guidelines. The focus is on a secure, multiplayer-enabled Pong platform, with options for expansion into advanced gameplay and improved user experience through additional, optional modules.

## Introduction

Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It is built by experienced developers to make web development easier by handling many of the common web development tasks, such as handling database connections, rendering HTML, managing user sessions, and much more. Django follows the "Don't Repeat Yourself" (DRY) principle, promoting reusability and the use of less code to achieve more.

## Key Components of Django

### Models
- Models define the structure of the database, essentially mapping database tables to Python objects.
- Each model is a Python class that subclasses `django.db.models.Model`.
- Django automatically generates the necessary SQL statements to create and manage the database tables based on these models.

```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    published_date = models.DateField()
```

### URLs
- Django uses URL routing to map URL patterns to views. The `urls.py` file in your app or project is where you define these mappings.
- Each URL pattern is associated with a view function or class that handles the request.

```python
from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.book_list, name='book_list'),
    path('books/<int:id>/', views.book_detail, name='book_detail'),
]
```

### Views
- Views are the functions or classes that handle the logic for a particular URL route.
- A view receives an HTTP request, processes it, interacts with the model if needed, and returns an HTTP response.

```python
from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})
```

### Templates
- Templates are used to define the structure and layout of your HTML pages. They allow you to embed Django Template Language (DTL) to dynamically generate content.
- Templates are typically stored in a `templates` directory within your app.

```html
<!-- templates/books/book_list.html -->
<h1>Book List</h1>
<ul>
    {% for book in books %}
        <li>{{ book.title }} by {{ book.author }}</li>
    {% endfor %}
</ul>
```

### Middleware
- Middleware is a framework of hooks into Django's request/response processing. It's a lightweight, low-level "plugin" system for globally altering Django's input or output.
- Middleware is defined in the `MIDDLEWARE` setting in `settings.py`.

Example of common middleware:
- `django.middleware.security.SecurityMiddleware`: Enhances security.
- `django.middleware.csrf.CsrfViewMiddleware`: Provides Cross-Site Request Forgery protection.

### Forms
- Forms in Django are used to handle user input and validation. Forms can be generated either from a model (`ModelForm`) or can be created manually.

```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
```

### Static Files
- Static files are files like CSS, JavaScript, and images that aren't dynamically generated by Django.
- Django has a dedicated app called `django.contrib.staticfiles` that helps in managing static files.

```html
<!-- Including a static file in a template -->
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'css/styles.css' %}">
```

## Basic Django Commands

1. **Starting a New Django Project**
   ```bash
   django-admin startproject myproject
   ```
   - This command creates a new Django project with the necessary files and directory structure.

2. **Creating a New Django App**
   ```bash
   python manage.py startapp myapp
   ```
   - An app is a self-contained module that can be plugged into a project. This command sets up the basic structure for an app.

3. **Running the Development Server**
   ```bash
   python manage.py runserver
   ```
   - Starts the built-in Django development server to test your application locally.

4. **Making Migrations**
   ```bash
   python manage.py makemigrations
   ```
   - This command tells Django to create new migrations based on the changes you have made to your models.

5. **Applying Migrations**
   ```bash
   python manage.py migrate
   ```
   - Applies the migrations to the database, synchronizing the database schema with your models.

6. **Creating a Superuser**
   ```bash
   python manage.py createsuperuser
   ```
   - Creates a superuser account that can log in to the Django admin site.

7. **Collecting Static Files**
   ```bash
   python manage.py collectstatic
   ```
   - Gathers all static files from your apps into one directory, usually for deployment.

8. **Shell**
   ```bash
   python manage.py shell
   ```
   - Opens an interactive Python shell with the Django environment loaded, useful for testing and debugging.

## Migrations in Django

Migrations are Django's way of propagating changes you make to your models (adding a field, deleting a model, etc.) into your database schema. Migrations are stored as files on disk, and they allow Django to apply or unapply the changes you made to your database in a controlled manner.

- **Creating Migrations**: `python manage.py makemigrations`
  - This command generates migration files based on the changes detected in your models.
  
- **Applying Migrations**: `python manage.py migrate`
  - Applies the migration files to the database, updating the database schema.

- **Rollback Migrations**: `python manage.py migrate <app_name> <previous_migration_name>`
  - Allows you to revert to a previous migration, essentially undoing changes to the database.

## Transcendence Project Structure

The Transcendence project is structured as follows:

```
└── 📁Trans
    └── 📁Django
        └── 📁Code
            └── 📁Auth
                └── __init__.py
                └── admin.py
                └── apps.py
                └── models.py
                └── serializers.py
                └── urls.py
                └── views.py
            └── 📁backend
                └── __init__.py
                └── asgi.py
                └── middleware.py
                └── settings.py
                └── urls.py
                └── wsgi.py
            └── 📁media
                └── 📁Auth
                    └── 📁defaultAssets
                        └── ProfilePicture.png
            └── 📁Sockets
                └── __init__.py
                └── admin.py
                └── apps.py
                └── consumers.py
                └── models.py
                └── routing.py
                └── tests.py
                └── views.py
            └── 📁static
                └── 📁css
                    └── style.css
                └── 📁js
                    └── 📁Menu
                        └── index.js
            └── 📁WebApp
                └── 📁migrations
                    └── __init__.py
                └── 📁templates
                    └── 📁Components
                        └── Menu.html
                    └── index.html
                └── __init__.py
                └── admin.py
                └── apps.py
                └── models.py
                └── tests.py
                └── urls.py
                └── views.py
            └── manage.py
        └── Dockerfile
        └── requirements.txt
    └── 📁Nginx
        └── 📁Conf
            └── default.conf
        └── Dockerfile
    └── compose.yml
    └── export.md
    └── Makefile
    └── README.md
```

### Explanation:
- **Auth**: Handles user authentication, including models, views, and serializers for user data.
- **backend**: Contains the core settings and configurations for the Django project, including middleware, URLs, and WSGI/ASGI configuration.
- **media**: Contains media files, such as user-uploaded content.
- **Sockets**: Manages WebSocket connections, consumers, and routing.
- **static**: Contains static assets like CSS and JavaScript files.
- **WebApp**: Contains the core web application logic, including models, views, templates, and

- **GameComunication**: Contains the logic for handling game communication

```json
[
    //Output \/
    {
        "PlayerOne": {
            "xPercent": 0.5
        },
        "PlayerTwo": {
            "xPercent": 0.5
        },
        "Ball": {
            "xPercent": 0.5,
            "yPercent": 0.5
        },
        "Score": {
            "PlayerOne": 0,
            "PlayerTwo": 0
        },
        "GameState": {
            "GameRunning": true
        }
    },
    //Input \/
    {
        "GameEvent": {
            "PlayerOneScored": {
                "Event": [ "Up", "Down"]
            },
            "PlayerTwoScored": {
                "Event": [ "Up", "Down"]
            },
            "Event": [
                "PlayerOneScored",
                "PlayerTwoScored",
                "PlayerOneWon",
                "PlayerTwoWon",
                "GamePaused",
                "GameResumed"
            ]
        }
    }
]
```

 migrations.
- **Nginx**: Contains configuration files and Docker setup for the Nginx server.
- **compose.yml**: Docker Compose configuration for managing multi-container Docker applications.
- **Dockerfile**: Docker configurations for building the Django and Nginx images.
- **Makefile**: Contains useful commands for setting up and managing the project.

## Docker Concepts for the Project

The project utilizes Docker to manage and deploy the application across various containers. The Docker Compose file (`compose.yml`) defines the services required for the application to run:

```yaml
services:
  db:
    container_name: db
    image: postgres
    ports:
      - 5432:5432
    environment:
      POSTGRES_PASSWORD: example
    networks:
      - default

  redis-server:
    container_name: redis-server
    command: redis-server
    image: redis
    ports:
      - 6379:6379
    networks:
      - default

  django:
    container_name: Django
    build: ./Django
    command: bash -c "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"
    volumes:
      - ./Django/Code/:/code/
    ports:
      - 8000:8000
    depends_on:
      - db
      - redis-server
    networks:
      - default

  web:
    container_name: Nginx
    build: ./Nginx
    ports:
      - 80:80
      - 443:443
    volumes:
      - ./Django/Code/static/:/static/
    depends_on:
      - django
    networks:
      - default
    
  pgadmin:
    container_name: pgadmin
    image: dpage/pgadmin4
    ports:
      - 5050:80
    volumes:
      - ../Db/pgadmin:/root/.pgadmin
      - ../Db/pgdata:/var/lib/postgresql/data
      - ../Db/pgadmin:/var/lib/pgadmin
    environment:
      PGADMIN_DEFAULT_EMAIL: pgadmin@pgadmin.org
      PGADMIN_DEFAULT_PASSWORD: pgadmin

volumes:
  static_volume:

networks:
  default:
```

### Services:
- **db**: A PostgreSQL container that serves as the database for the Django application.
- **redis-server**: A Redis container used for caching and session management.
- **django**: The main Django application container. It depends on the `db` and `redis-server` services and runs the development server.
- **web**: An Nginx container that serves as a reverse proxy for the Django application.
- **pgadmin**: A container running pgAdmin, a web-based interface for managing PostgreSQL databases.

### Volumes and Networks:
- **Volumes**: Persistent storage for the database and static files.
- **Networks**: Internal communication between containers.

## Setting Up and Running the Project

### Prerequisites:
- Docker and Docker Compose installed on your machine.

### Steps:

1. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd Trans
   ```

2. **Build and Start the Containers:**
   ```bash
   docker-compose up --build
   ```

3. **Access the Application:**
   - Django: `http://localhost:8000`
   - Nginx: `http://localhost`
   - pgAdmin: `http://localhost:5050`

4. **Create a Superuser:**
   ```bash
   docker exec -it Django python manage.py createsuperuser
   ```

5. **Collect Static Files:**
   ```bash
   docker exec -it Django python manage.py collectstatic
   ```

## Deployment

To deploy the Transcendence project, ensure that your production server is set up with Docker and Docker Compose. Modify environment variables in the `compose.yml` file to suit your production environment and follow the steps mentioned in the [Setting Up and Running the Project](#setting-up-and-running-the-project) section.

For securing your Nginx server with SSL, you can integrate Let's Encrypt or another SSL provider by configuring the `Nginx` Dockerfile and `default.conf`.

## Conclusion

This README serves as a comprehensive guide to understanding and working with the Transcendence project. Whether you are setting up the project locally for development or deploying it to a production environment, this documentation provides the necessary steps and insights to get started.




# Changes

## Date: 18 Jan

It's possible to update the intra faster.

inside of the .env you will have the following keys:
```.env
INTRA_CLIENT_ID= # Your Id
INTRA_CLIENT_SECRET= # Secrete token
INTRA_REDIRECT_URI= # Call back
```

Because of that everytime you have to generate new things its faster to update and secure. 
If any case you update the values you have to restart the containers by running the `make restart` or `make down` and after `make all`

Also it was created a folder commands and a py files that will do a specific thing.

in this case it was created a setupEnv.py that will apply the ip address on the .env

How to use 

```bash
python3 -m venv {enviroment folder name}
source enviroment/bin/activate
python3 commands/setupEnv.py
```




