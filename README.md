# ft_transcendence


<!-- ## USE THE PYTHON ENVIROMENT VIRTUAL > https://docs.python.org/3/library/venv.html -->


### Python Enviroment Setup

```shell
python3 -m venv name
source name/bin/activate
```

In case of any error check if you have all the dependencies. [Link](https://reintech.io/blog/install-python3-pip-debian-12)

### Django Structure.

What is called `Project` is where is the whole project. The `App` is the **application** that will be used on the `Project` 

Example:

- WebSite:
    - > Login
    - > Chat
    - > User Management


Here is some basic commands, I suggest to search and mess around with the framework to get to know.

```sh
#Setup the Project require the django admin installed on the Python Enviroment pip
django-admin startproject myproject
#Start the server
python manage.py runserver
#Setup an application inside the current project.
python manage.py startapp blog
```

#### The Django DB
Django has an integrated database, that means that you can having a saved database for you logins you chat what ever you have.

For each app you have a `model.py` each model represents a table of the database. If you trying to create or update a database, be carefull to always backup first. and run the following commands.

```sh
#this will update the database and append a table, or update etc... on cache
python manage.py makemigrations <appname> 


#this will access for each app cache and update based on the things changed.
pythob manage.py migrate 

#In case of listing the changes maded. this command will help you see the migrations
python manage.py showmigrations
```

#### Django Administration.

Django has a integretaed Django Administration panel, here you will be able to update, craate data that represents you models. Let's say you have a model that will store just a name, You can create a user called "Pedro" for example and will be updated on the database. For those who already know some database managment it would be something like `INSET INTO (x) VALUES (x); commit`. Something around that. 

In Django A Model is just a class that have his own attributes etc...