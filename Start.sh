#!/bin/bash

cd backend  


python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
pip install -r requirements.txt


cd ../frontend

npm i 



wall "
    Installation is done
    Basic commands on the backend:
    - cd backend -> to go to the backend folder
    - source env/bin/activate -> to activate the virtual environment
    - deactivate -> to deactivate the virtual environment
    =========== DJANGO COMMANDS ===========

    - python3 manage.py runserver -> to run the server
    - python3 manage.py makemigrations -> to create migrations
    - python3 manage.py migrate -> to apply migrations

    Basic commands on the frontend:
    - cd frontend -> to go to the frontend folder
    - npm run dev -> to run the server
    - npm run build -> to build the project
    - npm run preview -> to preview the project
"
