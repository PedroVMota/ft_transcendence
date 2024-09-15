# **Authentication and User Management API**

This project implements a basic authentication system using Django, allowing users to register, log in, and manage their sessions. The API supports CSRF-protected authentication and includes endpoints for retrieving user details and closing sessions.

## **Features**
- User registration
- User login (CSRF-protected)
- Session management (login/logout)
- Retrieve authenticated user details

## **Endpoints**

### **1. User Login**
- **URL**: `/auth/token/login/`
- **Method**: `POST`
- **Description**: Logs in a user and creates a session.
- **Request Body**:
  ```json
  {
      "username": "your-username",
      "password": "your-password"
  }
  ```
- **Response**:
  - Success: Returns a success message with `200 OK`.
  - Failure: Returns an error message with `400 Bad Request` or `500 Internal Server Error`.

### **2. Get CSRF Token**
- **URL**: `/auth/token/login/`
- **Method**: `GET`
- **Description**: Retrieves a CSRF token for secure requests.

### **3. User Registration**
- **URL**: `/auth/token/register/`
- **Method**: `POST`
- **Description**: Registers a new user.
- **Request Body**:
  ```json
  {
      "username": "new-username",
      "password": "password",
      "password2": "password-confirm",
      "email": "email@example.com"
  }
  ```
- **Response**:
  - Success: Returns a success message with `201 Created`.
  - Failure: Returns an error message with `400 Bad Request` or `500 Internal Server Error`.

### **4. Logout / Close Session**
- **URL**: `/auth/token/flush/`
- **Method**: `POST`
- **Description**: Logs out the authenticated user and closes their session.

### **5. Get User Details**
- **URL**: `/auth/user/`
- **Method**: `GET`
- **Description**: Retrieves the details of the currently authenticated user.
- **Response**:
  ```json
  {
      "user": {
          "username": "your-username",
          "email": "your-email@example.com"
      }
  }
  ```
