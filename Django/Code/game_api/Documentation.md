# **Game Room API Documentation**

### **Model: `GameRoom`**

The `GameRoom` model represents a game room where players can join to play a game, and spectators can watch. It contains fields for game name, state, privacy, players, spectators, and other metadata like room ID and WebSocket UUID.

---

### **Endpoints**

#### 1. **Generate Game Room**
- **URL**: `/game/generate/`
- **Method**: `POST`
- **Authentication**: Required (Authenticated users only)

##### **Request**:
```json
{
    "Name": "Optional Game Room Name"
}
```
- `Name`: Optional. If not provided, the default name "Game Room" is used.

##### **Response**:
- **Success** (201 - Created):
```json
{
    "Name": "Game Room Name",
    "State": 2,  // 2 = Not Started
    "Privacy": 1,  // 1 = Public
    "GameWebSoocket": "uuid-string-for-websocket",
    "RoomId": "uuid-string-for-room-id",
    "PlayerOne": "player-one-username",
    "PlayerTwo": null,
    "Spectators": [],
    "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
}
```

- **Errors**:
    - **403 Forbidden** (User is not authenticated):
    ```json
    {
        "error": "Forbidden"
    }
    ```
    - **400 Bad Request** (Invalid request method):
    ```json
    {
        "error": "Invalid request method"
    }
    ```

---

#### 2. **Get Game Rooms**
- **URL**: `/game/get/`
- **Method**: `GET`
- **Authentication**: Required (Authenticated users only)

##### **Request**:
No request body required.

##### **Response**:
- **Success** (200 - OK):
```json
[
    {
        "Name": "Game Room Name 1",
        "State": 1,  // 1 = In Progress
        "Privacy": 1,  // 1 = Public
        "GameWebSoocket": "uuid-string-for-websocket-1",
        "RoomId": "uuid-string-for-room-id-1",
        "PlayerOne": "player-one-username",
        "PlayerTwo": "player-two-username",
        "Spectators": ["spectator1-username", "spectator2-username"],
        "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
    },
    {
        "Name": "Game Room Name 2",
        "State": 2,  // 2 = Not Started
        "Privacy": 2,  // 2 = Private
        "GameWebSoocket": "uuid-string-for-websocket-2",
        "RoomId": "uuid-string-for-room-id-2",
        "PlayerOne": "another-player-username",
        "PlayerTwo": null,
        "Spectators": [],
        "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
    }
]
```

- **Errors**:
    - **403 Forbidden**:
    ```json
    {
        "error": "Forbidden"
    }
    ```
    - **400 Bad Request**:
    ```json
    {
        "error": "Invalid request method"
    }
    ```

---

#### 3. **Join Game Room**
- **URL**: `/game/join/`
- **Method**: `POST`
- **Authentication**: Required (Authenticated users only)

##### **Request**:
```json
{
    "RoomId": "uuid-string-for-room-id"
}
```
- `RoomId`: Required. The unique identifier of the room the user wants to join.

##### **Response**:
- **Success** (200 - OK):
```json
{
    "Name": "Game Room Name",
    "State": 1,  // 1 = In Progress
    "Privacy": 1,  // 1 = Public
    "GameWebSoocket": "uuid-string-for-websocket",
    "RoomId": "uuid-string-for-room-id",
    "PlayerOne": "player-one-username",
    "PlayerTwo": "player-two-username",
    "Spectators": [],
    "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
}
```

- **Errors**:
    - **403 Forbidden**:
    ```json
    {
        "error": "Forbidden"
    }
    ```
    - **400 Bad Request** (Missing `RoomId`):
    ```json
    {
        "error": "RoomId is required"
    }
    ```
    - **404 Not Found**:
    ```json
    {
        "error": "Room does not exist"
    }
    ```
    - **201 Conflict** (User is already a player):
    ```json
    {
        "error": "User is already a player"
    }
    ```

---

#### 4. **Leave Game Room**
- **URL**: `/game/leave/`
- **Method**: `POST`
- **Authentication**: Required (Authenticated users only)

##### **Request**:
```json
{
    "RoomId": "uuid-string-for-room-id"
}
```
- `RoomId`: Required. The unique identifier of the room the user wants to leave.

##### **Response**:
- **Success** (200 - OK):
```json
{
    "Name": "Game Room Name",
    "State": 2,  // 2 = Not Started
    "Privacy": 1,  // 1 = Public
    "GameWebSoocket": "uuid-string-for-websocket",
    "RoomId": "uuid-string-for-room-id",
    "PlayerOne": "player-one-username",
    "PlayerTwo": null,
    "Spectators": [],
    "Doc": "The Room ID is the unique identifier for the room, the GameWebSocket is the unique identifier for the game websocket."
}
```

- **Errors**:
    - **403 Forbidden**:
    ```json
    {
        "error": "Forbidden"
    }
    ```
    - **400 Bad Request** (Missing `RoomId`):
    ```json
    {
        "error": "RoomId is required"
    }
    ```
    - **404 Not Found**:
    ```json
    {
        "error": "Room does not exist"
    }
    ```
    - **201 Conflict** (User is not a player):
    ```json
    {
        "error": "User is not a player"
    }
    ```

---

### **GameRoom Model Fields**

- `id`: Auto-incremented primary key.
- `GameName`: The name of the game room.
- `GameStates`: Represents the current state of the game. Possible values:
  - `1`: In Progress
  - `2`: Not Started (default)
  - `3`: Completed
- `GamePrivacy`: Represents the privacy setting of the game. Possible values:
  - `1`: Public (default)
  - `2`: Private
- `websocketUuid`: A unique UUID used to identify the WebSocket connection for this game.
- `roomId`: A unique UUID used to identify the game room.
- `PlayerOne`: The user who created the game room (optional initially).
- `PlayerTwo`: The user who joins the game room to play against PlayerOne (optional initially).
- `GameChat`: The chat object associated with this game room, linking players for communication.
- `Spectators`: A many-to-many relationship with users who are spectating the game.