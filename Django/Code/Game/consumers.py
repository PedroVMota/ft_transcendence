# Sockets/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

from Game.Game import gameInstance

"""
[
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
        }cp
    }
]
"""

# class PongGameConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         # Get the room name from the URL route
#         self.room_name = self.scope['url_route']['kwargs']['room_name']
#         self.room_group_name = f'pong_{self.room_name}'

#         # Add the WebSocket connection to the group (room)
#         await self.channel_layer.group_add(
#             self.room_group_name,
#             self.channel_name
#         )

#         # Accept the WebSocket connection
#         await self.accept()

#     async def disconnect(self, close_code):
#         # Remove the WebSocket connection from the group
#         await self.channel_layer.group_discard(
#             self.room_group_name,
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         # Load the received text data into a Python dictionary
#         data = json.loads(text_data)

#         # Print the received data from the client
#         print("Received Data from client: ", json.dumps(data, indent=4))

#         # Broadcast the received data to all users in the room
#         await self.channel_layer.group_send(
#             self.room_group_name,
#             {
#                 'type': 'game_update',  # This will trigger the game_update method for all clients
#                 'data': data  # Send the data received from the client to the room
#             }
#         )

#     async def game_update(self, event):
#         # Extract the data that was sent by the client
#         received_data = event['data']

#         # Print the event data for debugging
#         print("Broadcasted Event Data: ", json.dumps(received_data, indent=4))

#         # Game event, representing the updated game state (this can be dynamic in a real game)
#         GameEvent: dict = {
#             "PlayerOne": {
#                 "xPercent": 0.5
#             },
#             "PlayerTwo": {
#                 "xPercent": 0.5
#             },
#             "Ball": {
#                 "xPercent": 0.5,
#                 "yPercent": 0.5
#             },
#             "Score": {
#                 "PlayerOne": 0,
#                 "PlayerTwo": 0
#             },
#             "GameState": {
#                 "GameRunning": True
#             }
#         }
#         # Combine the received data from the client and the game event
#         combined_data = {
#             "ClientData": received_data,  # Data received from the client
#             "GameEvent": GameEvent  # Static or dynamically updated game state
#         }
#         # Print the data before sending it to the client
#         print("Sending to client: ", json.dumps(combined_data, indent=4))
#         # Send the combined data (received input and the game event) back to the client
#         await self.send(text_data=json.dumps(combined_data))














"""
{
    "uuid": "c0d84804-b5d5-4409-aaa8-79024bb13fb2",
    "PlayerOne": "John",
    "PlayerTwo": "Jane",
    "Winner": null,
    "State": "In Progress",
    "TypeGame": "Friendly"
}
"""

class MonitorGameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("connect")
        if self.scope["user"].is_anonymous:
            await self.close()
        # check if the user has a superuser status
            if not self.scope["user"].is_superuser:
                await self.close()
        else:
            self.room_group_name = 'Monitor_Game'

            # Add the WebSocket connection to the group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            # Send a message back to the client confirming the connection
            await self.send(text_data=json.dumps({
                "type": "websocket.accept",
                "message": "You are now connected!"
            }))

    async def disconnect(self, close_code):
        print("disconnect")

        # Send a disconnect message (optional)
        await self.send(text_data=json.dumps({
            "type": "websocket.close",
            "message": f"You have been disconnected! Code: {close_code}"
        }))

        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @staticmethod
    def handle_score_bar_update(data):
        player_one = {}
        player_two = {}
        player_one['name'] = 'Zé'
        player_one['score'] = 0
        player_two['name'] = 'Adilson'
        player_two['score'] = 1
        data['playerOne'] = player_one
        data['playerTwo'] = player_two

    @staticmethod
    def handle_movement_key_press_notification(player, key):
        if player == 0:
            gameInstance.playerOne.handle_movement_key(key)
        if player == 1:
            gameInstance.playerTwo.handle_movement_key(key)

    @staticmethod
    def handle_camera_key_press_notification(player, key):
        if player == 0:
            gameInstance.playerOne.camera.

    @staticmethod
    def report_game_state(data):
        data["action"] = "game-state-report"
        data["ball"] = gameInstance.ball.get_dict()
        data["playerOne"] = gameInstance.playerOne.get_dict()
        data["playerTwo"] = gameInstance.playerTwo.get_dict()


    async def receive(self, text_data):
        print("receive")
        # Receive and process the incoming WebSocket message
        data = json.loads(text_data)

        if data["action"] == "score-bar-update":
            print("action is score-bar-update")
            self.handle_score_bar_update(data)
            print(data)

        if data["action"] == "movement-key-press-notification":
            print("action is movement-key-press-notification")
            self.handle_movement_key_press_notification(data["player"], data["message"])
            self.report_game_state(data)
            print(data)

        # Broadcast the message to all WebSocket connections in the group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "websocket.message",
                "message": data
            }
        )

    async def websocket_message(self, event):
        print("websoket_message")
        # This is called when a message is received from the group
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_accept(self, event):
        print("websocket_accept")
        # Handle WebSocket connection accept event
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_close(self, event):
        print("websocket_close")
        # Handle WebSocket connection close event
        await self.send(text_data=json.dumps(event["message"]))