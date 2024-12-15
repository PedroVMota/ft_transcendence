# Sockets/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import json

from Game.Game import gameInstance

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
    def report_score_bar(data):
        player_one = {}
        player_two = {}
        player_one['name'] = gameInstance.loop.game.playerOne.name
        player_one['score'] = gameInstance.loop.game.playerOne.score
        player_two['name'] = gameInstance.loop.game.playerTwo.name
        player_two['score'] = gameInstance.loop.game.playerTwo.score
        data['action'] = 'score-bar-report'
        data['playerOne'] = player_one
        data['playerTwo'] = player_two

    # @staticmethod
    # def handle_movement_key_press_notification(player, key):
    #     if player == 0:
    #         gameInstance.loop.game.playerOne.handle_paddle_movement(key)
    #     if player == 1:
    #         gameInstance.loop.game.playerTwo.handle_paddle_movement(key)
    #
    # @staticmethod
    # def handle_camera_key_press_notification(player, key):
    #     if player == 0:
    #         gameInstance.loop.game.playerOne.camera.handle_paddle_movement()

    @staticmethod
    def report_game_state(data):
        data["action"] = "game-state-report"
        data["ball"] = gameInstance.loop.game.ball.get_dict()
        data["playerOne"] = gameInstance.loop.game.playerOne.get_pos()
        data["playerTwo"] = gameInstance.loop.game.playerTwo.get_pos()


    @staticmethod
    def handle_paddle_move(data):
        if gameInstance.loop.game.running:
            if data["player"] == 0:
                gameInstance.loop.game.playerOne.handle_paddle_movement(data["direction"])
            elif data["player"] == 1:
                gameInstance.loop.game.playerTwo.handle_paddle_movement(data["direction"])



    async def receive(self, text_data):
        print("receive")
        # Receive and process the incoming WebSocket message
        data = json.loads(text_data)

        if data["action"] == "paddle-move-notification":
            print("received paddle-move-notification")
            self.handle_paddle_move(data)

        if data["action"] == "game-state-request":
            print("received game-state-request")
            self.report_game_state(data)


        if data["action"] == "score-bar-update-request":
            print("action is score-bar-update")
            self.report_score_bar(data)

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