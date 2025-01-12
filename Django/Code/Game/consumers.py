# Sockets/consumers.py
import json
from channels.layers import get_channel_layer
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils.decorators import sync_only_middleware

from Auth.models import MyUser
from Game.models import Game as GameModel
from Game.models import Lobby as LobbyModel
from Game.models import GameHistory as GameHistoryModel
from django.conf import settings
import redis

from Game.Game import GameInstance, activeGames, aiGames


class MonitorGameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created = False

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

            user_dict = await sync_to_async(self.scope["user"].getDict)()
            user_code = user_dict['Info']['userCode']

            if self.created is False:
                aiGames[user_code] = GameInstance(aiIncluded=True)
                self.created = True

            # Send a message back to the client confirming the connection
            await self.send(text_data=json.dumps({
                "type": "websocket.accept",
                "message": "You are now connected!"
            }))

    @staticmethod
    def report_score_bar(data, user_code):
        player_one = {}
        player_two = {}
        player_one['name'] = aiGames[user_code].loop.game.playerOne.name
        player_one['score'] = aiGames[user_code].loop.game.playerOne.score
        player_two['name'] = "Crazy AI"
        player_two['score'] = aiGames[user_code].loop.game.playerTwo.score
        data['action'] = 'score-bar-report'
        data['playerOne'] = player_one
        data['playerTwo'] = player_two

    # @staticmethod
    # def handle_movement_key_press_notification(player, key):
    #     if player == 0:
    #         aiGames[user_code].loop.game.playerOne.handle_paddle_movement(key)
    #     if player == 1:
    #         aiGames[user_code].loop.game.playerTwo.handle_paddle_movement(key)
    #
    # @staticmethod
    # def handle_camera_key_press_notification(player, key):
    #     if player == 0:
    #         aiGames[user_code].loop.game.playerOne.camera.handle_paddle_movement()

    @staticmethod
    def report_game_state(data, user_code):
        data["action"] = "game-state-report"
        data["ball"] = aiGames[user_code].loop.game.ball.get_dict()
        data["playerOne"] = aiGames[user_code].loop.game.playerOne.get_pos()
        data["playerTwo"] = aiGames[user_code].loop.game.playerTwo.get_pos()

    async def disconnect(self, close_code):
        print("disconnect")
        user_dict = await sync_to_async(self.scope["user"].getDict)()
        user_code = user_dict['Info']['userCode']
        if aiGames[user_code] is not None:
            del aiGames[user_code]
            aiGames.pop(user_code)
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
    def handle_paddle_move(data, user_code):
        if aiGames[user_code].loop.game.playing:
            if data["player"] == 0:
                aiGames[user_code].loop.game.playerOne.handle_paddle_movement(data["direction"])
            # elif data["player"] == 1:
            #     aiGames[user_code].loop.game.playerTwo.handle_paddle_movement(data["direction"])


    async def receive(self, text_data):
        print("receive")
        # Receive and process the incoming WebSocket message
        data = json.loads(text_data)

        user_dict = await sync_to_async(self.scope["user"].getDict)()
        user_code = user_dict['Info']['userCode']

        if data["action"] == "paddle-move-notification":
            #print("received paddle-move-notification")
            self.handle_paddle_move(data, user_code)

        if data["action"] == "game-state-request":
            #print("received game-state-request")
            self.report_game_state(data, user_code)

        if data["action"] == "score-bar-update-request":
            #print("action is score-bar-update")
            self.report_score_bar(data, user_code)

        if data["action"] == "request-pause-play":
                print("action is request-pause-play")
                if aiGames[user_code].loop.game.playing:
                    aiGames[user_code].loop.game.playing = False
                else:
                    aiGames[user_code].loop.game.playing = True

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
        #print("websoket_message")
        # This is called when a message is received from the group
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_accept(self, event):
        #print("websocket_accept")
        # Handle WebSocket connection accept event
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_close(self, event):
        #print("websocket_close")
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
    def __init__(self):
        self.created = False

    async def connect(self):
        self.finished = False
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

            if self.created is False:
                game_model = await sync_to_async(GameModel.objects.filter)(id=self.room_group_name)
                game_model = await sync_to_async(game_model.get)()
                game_model_dict = await sync_to_async(game_model.getDict)()
                player_one = game_model_dict["PlayerOne"]
                player_two = game_model_dict["PlayerTwo"]
                self.created = True

                activeGames[self.room_group_name] = GameInstance(player_one['Info']['userCode'], player_two['Info']['userCode']
                                                             ,player_one['Info']['first_name'], player_two['Info']['first_name'])
            # Send a message back to the client confirming the connection
            await self.send(text_data=json.dumps({
                "type": "websocket.accept",
                "message": "You are now connected!"
            }))


    async def disconnect(self, close_code):
        print("DISCONNECTING")

        # Send a disconnect message (optional)
        await self.send(text_data=json.dumps({
            "type": "websocket.close",
            "message": f"You have been disconnected! Code: {close_code}"
        }))
        if activeGames[self.room_group_name] is not None:
            del activeGames[self.room_group_name]
            #activeGames.pop(self.room_group_name)

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

    async def register_to_history(self, winner):
        game_model = await sync_to_async(GameModel.objects.filter)(id=self.room_group_name)
        game_model = await sync_to_async(game_model.get)()
        p1_score = activeGames[self.room_group_name].loop.game.playerOne.score
        p2_score = activeGames[self.room_group_name].loop.game.playerTwo.score
        winner_p = None
        if winner == 1:
            winner_p = game_model.pOne
        elif winner == 2:
            winner_p = game_model.pTwo
        history = GameHistoryModel(game_id=str(game_model.id), playerOne=game_model.pOne, playerTwo=game_model.pTwo, winner=winner_p, playerOneScore=p1_score, playerTwoScore=p2_score)
        history.save()


    async def check_for_victories(self, data):
        winner_n = 0
        if activeGames[self.room_group_name].loop.game.playerOne.score >= 7:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].loop.game.playing = False
            winner_n = 1
        elif activeGames[self.room_group_name].loop.game.playerTwo.score >= 7:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].loop.game.playing = False
            winner_n = 2
        if winner_n != 0:
            print("registering-to-history")
            await self.register_to_history(winner_n)
            self.finished = True
            await self.close(1000)

    async def receive(self, text_data):
        data = json.loads(text_data)

        if not self.finished:
            if data["action"] == "paddle-move-notification":
                await self.handle_paddle_move(data)

            if data["action"] == "game-state-request":
                self.report_game_state(data)

            if data["action"] == "score-bar-update-request":
                self.report_score_bar(data)

            if data["action"] == "check-for-victory":
                await self.check_for_victories(data)

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
        if self.scope["user"].is_anonymous:
            await self.close()
            if not self.scope["user"].is_superuser:
                await self.close()
        else:
            self.room_group_name = self.scope['url_route']['kwargs']['lobby_id']
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            lobbyusers = await sync_to_async(lambda: list(LobbyModel.objects.filter(players=self.scope['user'])))()
            if lobbyusers:
                print("User already in the lobby")
                return
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "notification",
                    "message": f"Player {self.scope['user'].first_name} has joined the lobby",
                    "data": {
                        "userCode": self.scope['user'].userSocialCode,
                        "first_name": self.scope['user'].first_name,
                        "last_name": self.scope['user'].last_name,
                        "profile_picture": self.scope['user'].profile_picture.url,
                    }
                }
            )

    async def notification(self, event):
        message = event['message']
        data = event['data']
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'message': message,
            'data': data
        }))

    async def disconnect(self, close_code):
        # Redis key for the lobby
        redis_key = f"lobby:{self.scope['url_route']['kwargs']['lobby_id']}"
        # Fetch the existing data from Redis
        existing_data = await sync_to_async(redis_instance.get)(redis_key)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "notification",
                "message": f"Player {self.scope['user'].first_name} has left the lobby",
                "data": {}
            }
        )

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
        data= json.loads(text_data)
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