# Authentication API Documentation
# Authentication Endpoints Documentation

This document provides an overview of the authentication endpoints available in the Django application.

## Endpoints

### User Authentication

- **Login**
  - **URL:** `/token/login/`
  - **Method:** `POST`
  - **Description:** Authenticates a user and initiates a session.
  - **Request Body:**
    ```json
    {
      "username": "user",
      "password": "password"
    }
    ```
  - **Responses:**
    - `200 OK` - Login successful
      ```json
      {
        "message": "Login successful"
      }
      ```
    - `400 Bad Request` - Invalid username or password
      ```json
      {
        "error": "Invalid username or password"
      }
      ```
    - `400 Bad Request` - Invalid JSON data
      ```json
      {
        "error": "Invalid JSON data"
      }
      ```

- **Register**
  - **URL:** `/token/register/`
  - **Method:** `POST`
  - **Description:** Registers a new user.
  - **Request Body:**
    ```json
    {
      "username": "user",
      "password": "password",
      "password2": "password"
    }
    ```
  - **Responses:**
    - `201 Created` - Registration successful
      ```json
      {
        "message": "Registration successful"
      }
      ```
    - `400 Bad Request` - Validation errors (e.g., missing fields, passwords do not match, username already exists)
      ```json
      {
        "error": "All fields are required"
      }
      ```
      ```json
      {
        "error": "Passwords do not match"
      }
      ```
      ```json
      {
        "error": "Username already exists"
      }
      ```
    - `400 Bad Request` - Invalid JSON data
      ```json
      {
        "error": "Invalid JSON"
      }
      ```

- **Logout**
  - **URL:** `/token/flush/`
  - **Method:** `POST`
  - **Description:** Logs out the authenticated user and closes the session.
  - **Responses:**
    - `200 OK` - Session closed
      ```json
      {
        "message": "Session closed"
      }
      ```
    - `401 Unauthorized` - No active session
      ```json
      {
        "message": "No active session"
      }
      ```

### User Information

- **Get User Data**
  - **URL:** `/token/user/`
  - **Method:** `GET`
  - **Description:** Retrieves information about the authenticated user.
  - **Responses:**
    - `200 OK` - User data
      ```json
      {
        "user_id": 1,
        "username": "user",
        "usercode": 1234,
        "email": "user@example.com",
        "first_name": "First",
        "last_name": "Last",
        "profile_picture": "/path/to/profile_picture.png",
        "about_me": "About me text",
        "create_date": "2023-10-01T00:00:00Z",
        "update_date": "2023-10-01T00:00:00Z",
        "friendlist": ["friend1", "friend2"],
        "blocked_users": ["blocked_user1"]
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

- **Update User Data**
  - **URL:** `/token/user/update/`
  - **Method:** `POST`
  - **Description:** Updates the authenticated user's profile.
  - **Request Body:** JSON object with user fields to update.
    ```json
    {
      "first_name": "New First",
      "last_name": "New Last",
      "about_me": "New about me text",
      "profile_picture": "new_profile_picture.png"
    }
    ```
  - **Responses:**
    - `200 OK` - Profile updated successfully
      ```json
      {
        "message": "Profile updated successfully!"
      }
      ```
    - `400 Bad Request` - Invalid data format or unsupported file extension
      ```json
      {
        "error": "Invalid data format."
      }
      ```
      ```json
      {
        "error": "Unsupported file extension. Allowed extensions are: png, webp, gif, jpg, jpeg"
      }
      ```
    - `405 Method Not Allowed` - Invalid request method
      ```json
      {
        "error": "Invalid request method. Only POST is allowed."
      }
      ```
    - `500 Internal Server Error` - Failed to update profile
      ```json
      {
        "error": "Failed to update profile."
      }
      ```

### Friends Management

- **Get Block List**
  - **URL:** `/token/block_list/`
  - **Method:** `GET`
  - **Description:** Retrieves the list of blocked users.
  - **Responses:**
    - `200 OK` - Block list
      ```json
      [
        "blocked_user1",
        "blocked_user2"
      ]
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

- **Block User**
  - **URL:** `/token/block/<int:socialCode>/`
  - **Method:** `POST`
  - **Description:** Blocks a user by their social code.
  - **Responses:**
    - `200 OK` - User blocked
      ```json
      {
        "message": "User blocked"
      }
      ```
    - `404 Not Found` - User not found
      ```json
      {
        "error": "User not found"
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

- **Remove Friend**
  - **URL:** `/token/remove/<int:socialCode>/`
  - **Method:** `POST`
  - **Description:** Removes a friend by their social code.
  - **Responses:**
    - `200 OK` - Friend removed
      ```json
      {
        "message": "Friend removed"
      }
      ```
    - `404 Not Found` - User not found
      ```json
      {
        "error": "User not found"
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

### Friend Requests

- **Send Friend Request**
  - **URL:** `/token/friend/request/send/`
  - **Method:** `POST`
  - **Description:** Sends a friend request to a user.
  - **Request Body:** JSON object with the target user's social code.
    ```json
    {
      "user_code": 1234
    }
    ```
  - **Responses:**
    - `200 OK` - Friend request sent successfully
      ```json
      {
        "message": "Friend request sent successfully!"
      }
      ```
    - `400 Bad Request` - Validation errors (e.g., cannot send request to self, request already sent)
      ```json
      {
        "error": "You cannot send a friend request to yourself"
      }
      ```
      ```json
      {
        "error": "Friend request already sent"
      }
      ```
    - `404 Not Found` - User not found
      ```json
      {
        "error": "User not found"
      }
      ```
    - `405 Method Not Allowed` - Invalid request method
      ```json
      {
        "error": "Invalid request method"
      }
      ```

- **Get Friend Requests**
  - **URL:** `/token/friend/request/get/`
  - **Method:** `GET`
  - **Description:** Retrieves pending friend requests for the authenticated user.
  - **Responses:**
    - `200 OK` - List of friend requests
      ```json
      {
        "friend_requests": [
          {
            "request_id": 1,
            "from_user": "user1",
            "from_user_id": 2,
            "from_user_profile_picture": "/path/to/profile_picture.png"
          }
        ]
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

- **Manage Friend Requests**
  - **URL:** `/token/friend/request/manage/`
  - **Method:** `POST`
  - **Description:** Accepts or rejects a friend request.
  - **Request Body:** JSON object with the friend request ID and action (`accept` or `reject`).
    ```json
    {
      "friend_request_id": 1,
      "action": "accept"
    }
    ```
  - **Responses:**
    - `200 OK` - Friend request accepted or rejected
      ```json
      {
        "message": "Friend request accepted"
      }
      ```
      ```json
      {
        "message": "Friend request rejected"
      }
      ```
    - `400 Bad Request` - Invalid action
      ```json
      {
        "error": "Invalid action"
      }
      ```
    - `404 Not Found` - Friend request not found
      ```json
      {
        "error": "Friend request not found"
      }
      ```
    - `405 Method Not Allowed` - Invalid request method
      ```json
      {
        "error": "Invalid request method"
      }
      ```

### Notifications

- **Get Notifications**
  - **URL:** `/token/notification/`
  - **Method:** `GET`
  - **Description:** Retrieves unread notifications for the authenticated user.
  - **Responses:**
    - `200 OK` - List of notifications
      ```json
      {
        "notifications": [
          {
            "message": "Notification message"
          }
        ]
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

### Chat Details

- **Get Chat Details**
  - **URL:** `/token/chat_details/`
  - **Method:** `GET`
  - **Description:** Retrieves chat details for the authenticated user.
  - **Responses:**
    - `200 OK` - List of chat details
      ```json
      {
        "chats": [
          {
            "username": "friend1",
            "email": "friend1@example.com",
            "profile_picture": "/path/to/profile_picture.png",
            "unique_id": "uuid",
            "targetUserUUID": 1234
          }
        ]
      }
      ```
    - `401 Unauthorized` - Not authenticated
      ```json
      {
        "error": "Not authenticated"
      }
      ```

## Models

### User
- **Fields:** `username`, `password`, `first_name`, `last_name`, `profile_picture`, `about_me`, `userSocialCode`

### FriendRequest
- **Fields:** `from_user`, `to_user`, `status`

### Notification
- **Fields:** `user`, `message`, `is_read`

### currentChat
- **Fields:** `members`, `unique_id`

## Utilities

- **accept_friend_request(request, friend_request)**
  - Accepts a friend request and creates a chat conversation.

- **reject_friend_request(friend_request)**
  - Rejects a friend request.

- **handle_friend_request(request)**
  - Handles sending a friend request.

## Notes

- All endpoints require the user to be authenticated unless otherwise specified.
- CSRF protection is disabled for these endpoints using the `@csrf_exempt` decorator.

For further details, refer to the source code and the Django documentation.