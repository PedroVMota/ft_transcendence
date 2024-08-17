import csv
import requests

# API endpoint
url = "https://localhost:443/auth/token/register/"

# CSV file containing user data
csv_file = 'users.csv'

# Function to register a user
def register_user(username, password, email):
    payload = {
        "username": username,
        "password": password,
        "email": email
    }
    try:
        response = requests.post(url, json=payload, verify=False)
        if response.status_code == 201:
            print(f"User {username} registered successfully.")
        else:
            print(f"Failed to register {username}. Status code: {response.status_code}, Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Read the CSV file and register each user
with open(csv_file, mode='r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        username = row['username']
        password = row['password']
        email = row['email']
        register_user(username, password, email)
