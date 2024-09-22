# Game API Documentation
## Description
This API allows users to interact with game rooms. Users can generate, retrieve, join, and leave game rooms. Authentication is required for all endpoints.

## Endpoints

### 1. Generate Game Room

**URL:** `/game/generate/`  
**Method:** `POST`  
**Request Body:**
```json
{
    "Name": "Game Room"
}
```

**Responses:**

- **201 Created**
  ```json
  {
      "Name": "Game Room",
      "State": 2,
      "Privacy": 1,
      "GameWebSocket": "<websocket_uuid>",
      "RoomId": "<room_id>",
      "PlayerOne": "<username>",
      "PlayerTwo": null,
      "Spectators": [],
      "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
  }
  ```

- **400 Bad Request**
  ```json
  {
      "error": "Invalid request method"
  }
  ```

- **403 Forbidden**
  ```json
  {
      "error": "Forbidden"
  }
  ```

### 2. Retrieve Game Rooms

**URL:** `/game/get/`  
**Method:** `GET`  

**Responses:**

- **200 OK**
  ```json
  [
      {
          "Name": "Game Room",
          "State": 2,
          "Privacy": 1,
          "GameWebSocket": "<websocket_uuid>",
          "RoomId": "<room_id>",
          "PlayerOne": "<username>",
          "PlayerTwo": null,
          "Spectators": [],
          "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
      }
  ]
  ```

- **400 Bad Request**
  ```json
  {
      "error": "Invalid request method"
  }
  ```

- **403 Forbidden**
  ```json
  {
      "error": "Forbidden"
  }
  ```

### 3. Join Game Room

**URL:** `/game/join/`  
**Method:** `POST`  
**Request Body:**
```json
{
    "RoomId": "<room_id>"
}
```

**Responses:**

- **200 OK**
  ```json
  {
      "Name": "Game Room",
      "State": 2,
      "Privacy": 1,
      "GameWebSocket": "<websocket_uuid>",
      "RoomId": "<room_id>",
      "PlayerOne": "<username>",
      "PlayerTwo": "<username>",
      "Spectators": [],
      "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
  }
  ```

- **400 Bad Request**
  ```json
  {
      "error": "RoomId is required"
  }
  ```

- **403 Forbidden**
  ```json
  {
      "error": "Forbidden"
  }
  ```

- **404 Not Found**
  ```json
  {
      "error": "Room does not exist"
  }
  ```

- **201 Created**
  ```json
  {
      "error": "User is already a player"
  }
  ```

### 4. Leave Game Room

**URL:** `/game/leave/`  
**Method:** `POST`  
**Request Body:**
```json
{
    "RoomId": "<room_id>"
}
```

**Responses:**

- **200 OK**
  ```json
  {
      "Name": "Game Room",
      "State": 2,
      "Privacy": 1,
      "GameWebSocket": "<websocket_uuid>",
      "RoomId": "<room_id>",
      "PlayerOne": null,
      "PlayerTwo": "<username>",
      "Spectators": [],
      "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
  }
  ```

- **400 Bad Request**
  ```json
  {
      "error": "RoomId is required"
  }
  ```

- **403 Forbidden**
  ```json
  {
      "error": "Forbidden"
  }
  ```

- **404 Not Found**
  ```json
  {
      "error": "Room does not exist"
  }
  ```

- **201 Created**
  ```json
  {
      "error": "User is not a player"
  }
  ```