# Sockets/consumers.py
import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils.decorators import sync_only_middleware

from Auth.models import MyUser
from Game.models import Game as GameModel
from django.conf import settings
import redis

from Game.Game import GameInstance, gameInstance, activeGames

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
        if gameInstance.loop.game.playing:
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
        print("sending data: ", data)
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





redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)

from asgiref.sync import sync_to_async



LobbyData = {
    "data" : {
        "GAME_STATE": "Waitting",
        "SizeOfPlayers": 0,
        "Player": {
            "PlayerOne": None,
            "PlayerTwo": None,
        }
    }
}

class MultiplayerGame(AsyncWebsocketConsumer):
    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        # check if the user has a superuser status
            if not self.scope["user"].is_superuser:
                await self.close()
        else:
            self.room_group_name = self.scope['url_route']['kwargs']['game_id']

            # Add the WebSocket connection to the group
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

            game_model = await sync_to_async(GameModel.objects.filter)(id=self.room_group_name)
            game_model = await sync_to_async(game_model.get)()
            game_model_dict = await sync_to_async(game_model.getDict)()
            player_one = game_model_dict["PlayerOne"]
            player_two = game_model_dict["PlayerTwo"]

            activeGames[self.room_group_name] = GameInstance(player_one['Info']['userCode'], player_two['Info']['userCode']
                                                             ,player_one['Info']['first_name'], player_two['Info']['first_name'])
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

    async def handle_paddle_move(self, data):
        if activeGames[self.room_group_name].loop.game.playing:
            user = await sync_to_async(self.scope["user"].getDict)()
            user_code = user["Info"]["userCode"]
            print("received handle_paddle_move from user: ", user_code)
            if user_code == activeGames[self.room_group_name].playerOne:
                print("moving player one with direction: ", data["direction"])
                activeGames[self.room_group_name].loop.game.playerOne.handle_paddle_movement(data["direction"])
            elif user_code == activeGames[self.room_group_name].playerTwo:
                print("moving player two with direction: ", data["direction"])
                activeGames[self.room_group_name].loop.game.playerTwo.handle_paddle_movement(data["direction"])


    def report_game_state(self, data):
        data["action"] = "game-state-report"
        data["ball"] = activeGames[self.room_group_name].loop.game.ball.get_dict()
        data["playerOne"] = activeGames[self.room_group_name].loop.game.playerOne.get_pos()
        data["playerTwo"] = activeGames[self.room_group_name].loop.game.playerTwo.get_pos()


    def report_score_bar(self, data):
        player_one = {}
        player_two = {}
        player_one['name'] =  activeGames[self.room_group_name].playerOneName
        player_one['score'] =  activeGames[self.room_group_name].loop.game.playerOne.score
        player_two['name'] =  activeGames[self.room_group_name].playerTwoName
        player_two['score'] =  activeGames[self.room_group_name].loop.game.playerTwo.score
        data['action'] = 'score-bar-report'
        data['playerOne'] = player_one
        data['playerTwo'] = player_two


    def check_for_victories(self, data):
        if activeGames[self.room_group_name].loop.game.playerOne.score >= 5:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].loop.game.playing = False
        elif activeGames[self.room_group_name].loop.game.playerTwo.score >= 5:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].loop.game.playing = False

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["action"] == "paddle-move-notification":
            await self.handle_paddle_move(data)

        if data["action"] == "game-state-request":
            self.report_game_state(data)

        if data["action"] == "score-bar-update-request":
            self.report_score_bar(data)

        if data["action"] == "check-for-victory":
            self.check_for_victories(data)

        if data["action"] == "request-pause-play":
            print("request-pause-play")
            if activeGames[self.room_group_name].loop.game.playing:
                activeGames[self.room_group_name].loop.game.playing = False
            else:
                activeGames[self.room_group_name].loop.game.playing = True


        # Broadcast the message to all WebSocket connections in the group
        #print("sending data: ", data)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "websocket.message",
                "message": data
            }
        )

    async def websocket_message(self, event):
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



# re_path(r'ws/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.LobbyConsumer.as_asgi()),
class MonitorLobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print('self room group name: ', self.scope['url_route']['kwargs'])
        if self.scope["user"].is_anonymous:
            await self.close()
        # check if the user has a superuser status
            if not self.scope["user"].is_superuser:
                await self.close()
        else:
            self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']

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
        # Redis key for the lobby
        redis_key = f"lobby:{self.scope['url_route']['kwargs']['lobby_id']}"

        # Fetch the existing data from Redis
        existing_data = await sync_to_async(redis_instance.get)(redis_key)

        if existing_data:
            # Decode and load the existing data
            decoded_result = existing_data.decode("utf-8")
            lobby_data = json.loads(decoded_result)

            # Decrement the SizeOfPlayers if greater than 0
            if lobby_data["data"]["SizeOfPlayers"] > 0:
                lobby_data["data"]["SizeOfPlayers"] -= 1

            # Save the updated data back to Redis
            updated_data = json.dumps(lobby_data)
            await sync_to_async(redis_instance.set)(redis_key, updated_data)

            print(f"Updated Lobby Data after disconnection: {updated_data}")
        else:
            print(f"Lobby data not found for key: {redis_key}")


    @staticmethod
    def handle_lobby_message(data, user):
        data["action"] = "lobby-message-submission"
        data["user"] = user['first_name']



    async def receive(self, text_data=None, bytes_data=None):
        print("receive")
        print(text_data)
        data=json.loads(text_data)
        user = await sync_to_async(self.scope["user"].getDict)()
        #print("consumer.receive printing its scope: ", user)
        #await sync_to_async(redis_instance.set)(redis_key, serialized_data)
        if data["action"] == "message-sent-on-lobby":
            self.handle_lobby_message(data, user['Info'])

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


# re_path(r'ws/Monitor/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.LobbyConsumer.as_asgi()),
class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
        self.user = self.scope['user']

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        # Send welcome message
        welcomeMsg = {
            'type': 'notification',
            'message': f"You have joined the lobby {self.room_group_name}"
        }
        await self.send(text_data=json.dumps(welcomeMsg))

        # Print and log the welcome message
        print(welcomeMsg['message'])

    async def disconnect(self, close_code):
        # Remove the user from the group
        goodbyeMsg = {
            'type': 'notification',
            'message': f"{self.user.username} has left the lobby"
        }
        await self.channel_layer.group_send(
            self.room_group_name,
            goodbyeMsg
        )
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        data['type'] = 'message'
        await self.channel_layer.group_send(
            self.room_group_name,
            data
        )

    async def notification(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message
        }))

    async def message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': message
        }))