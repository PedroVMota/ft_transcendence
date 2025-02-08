# Sockets/consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from Game.Game import GameInstance, activeGames, aiGames

from Auth.models import MyUser
from Game.models import Game as GameModel
from Game.models import GameHistory as GameHistoryModel

from django.conf import settings

from asgiref.sync import sync_to_async

import json
import redis

class GameConsumerIA(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.created = False
        self.room_group_name = None

    async def connect(self):
        if self.scope["user"].is_anonymous: # check if the user is anonymous
            await self.close()
        else:
            user_dictionary = await sync_to_async(self.scope["user"].getDict)()
            user_code = user_dictionary['Info']['userCode']
            self.room_group_name = 'Monitor_Game_' + str(user_code)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            if self.created is False:
                aiGames[user_code] = GameInstance(aiIncluded=True)
                self.created = True
            await self.send(text_data=json.dumps({
                "type": "websocket.accept",
                "message": "You are now connected!"
            }))

    @staticmethod
    def report_score_bar(data, user_code):
        player_one = {}
        player_two = {}
        player_one['name'] = aiGames[user_code].gameLoop.game.playerOne.name
        player_one['score'] = aiGames[user_code].gameLoop.game.playerOne.score
        player_two['name'] = "Crazy AI"
        player_two['score'] = aiGames[user_code].gameLoop.game.playerTwo.score
        data['action'] = 'score-bar-report'
        data['playerOne'] = player_one
        data['playerTwo'] = player_two

    @staticmethod
    def report_game_state(data, user_code):
        data["action"] = "game-state-report"
        data["ball"] = aiGames[user_code].gameLoop.game.ball.get_dict()
        data["playerOne"] = aiGames[user_code].gameLoop.game.playerOne.get_pos()
        data["playerTwo"] = aiGames[user_code].gameLoop.game.playerTwo.get_pos()

    async def disconnect(self, close_code):
        print("disconnect")
        user_model = await sync_to_async(self.scope["user"].get)()
        user_dict = await sync_to_async(user_model.getDict)()
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
        if aiGames[user_code].gameLoop.game.playing:
            if data["player"] == 0:
                aiGames[user_code].gameLoop.game.playerOne.handle_paddle_movement(data["direction"])


    async def receive(self, text_data):
        print("receive")
        # Receive and process the incoming WebSocket message
        data = json.loads(text_data)

        user_dict = await sync_to_async(self.scope["user"].getDict)()
        user_code = user_dict['Info']['userCode']

        if data["action"] == "paddle-move-notification":
            self.handle_paddle_move(data, user_code)

        if data["action"] == "game-state-request":
            self.report_game_state(data, user_code)

        if data["action"] == "score-bar-update-request":
            self.report_score_bar(data, user_code)

        if data["action"] == "request-pause-play":
                print("action is request-pause-play")
                if aiGames[user_code].gameLoop.game.playing:
                    aiGames[user_code].gameLoop.game.playing = False
                else:
                    aiGames[user_code].gameLoop.game.playing = True

        # Broadcast the message to all WebSocket connections in the group
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
        # Handle WebSocket connection accept event
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_close(self, event):
        # Handle WebSocket connection close event
        await self.send(text_data=json.dumps(event["message"]))


redis_instance = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0
)

LobbyData = {
    "data" : {
        "GAME_STATE": "Waiting",
        "SizeOfPlayers": 0,
        "Player": {
            "PlayerOne": None,
            "PlayerTwo": None,
        }
    }
}

class MultiplayerGame(AsyncWebsocketConsumer):
    def __init__(self):
        super().__init__()
        self.created = False
        self.room_group_name = ""
        self.finished = False

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


        try:
            if activeGames[self.room_group_name] is not None:
                del activeGames[self.room_group_name]
            #activeGames.pop(self.room_group_name)
        except KeyError:
            print("Error: Key not found")

        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def handle_paddle_move(self, data):
        if activeGames[self.room_group_name].gameLoop.game.playing:
            user = await sync_to_async(self.scope["user"].getDict)()
            user_code = user["Info"]["userCode"]
            print("received handle_paddle_move from user: ", user_code)
            if user_code == activeGames[self.room_group_name].playerOne:
                print("moving player one with direction: ", data["direction"])
                activeGames[self.room_group_name].gameLoop.game.playerOne.handle_paddle_movement(data["direction"])
            elif user_code == activeGames[self.room_group_name].playerTwo:
                print("moving player two with direction: ", data["direction"])
                activeGames[self.room_group_name].gameLoop.game.playerTwo.handle_paddle_movement(data["direction"])


    def report_game_state(self, data):
        data["action"] = "game-state-report"
        data["ball"] = activeGames[self.room_group_name].gameLoop.game.ball.get_dict()
        data["playerOne"] = activeGames[self.room_group_name].gameLoop.game.playerOne.get_pos()
        data["playerTwo"] = activeGames[self.room_group_name].gameLoop.game.playerTwo.get_pos()


    def report_score_bar(self, data):
        player_one = {}
        player_two = {}
        player_one['name'] =  activeGames[self.room_group_name].playerOneName
        player_one['score'] =  activeGames[self.room_group_name].gameLoop.game.playerOne.score
        player_two['name'] =  activeGames[self.room_group_name].playerTwoName
        player_two['score'] =  activeGames[self.room_group_name].gameLoop.game.playerTwo.score
        data['action'] = 'score-bar-report'
        data['playerOne'] = player_one
        data['playerTwo'] = player_two

    async def register_to_history(self, winner):
        game_model = await sync_to_async(GameModel.objects.filter)(id=self.room_group_name)
        game_model = await sync_to_async(game_model.get)()
        game_dict = await sync_to_async(game_model.getDict)()
        p1_score = activeGames[self.room_group_name].gameLoop.game.playerOne.score
        p2_score = activeGames[self.room_group_name].gameLoop.game.playerTwo.score
        winner_p = None
        print("type is", type(game_model))
        if winner == 1:
            winner_p = game_dict['PlayerOne']
        elif winner == 2:
            winner_p = game_dict['PlayerTwo']
        p_one = game_dict['PlayerOne']
        p_two = game_dict['PlayerTwo']
        history = GameHistoryModel(game_id=str(game_model.id), playerOne=str(p_one), playerTwo=str(p_two), winner=str(winner_p), playerOneScore=p1_score, playerTwoScore=p2_score)
        await sync_to_async(history.save)()


    async def check_for_victories(self, data):
        winner_n = 0
        if activeGames[self.room_group_name].gameLoop.game.playerOne.score >= 7:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].gameLoop.game.playing = False
            winner_n = 1
        elif activeGames[self.room_group_name].gameLoop.game.playerTwo.score >= 7:
            data["action"] = "game-win"
            data["victoriousPlayer"] = activeGames[self.room_group_name].playerTwoName
            activeGames[self.room_group_name].gameLoop.game.playing = False
            winner_n = 2
        if winner_n != 0:
            print("registering-to-history")
            #await self.register_to_history(winner_n)
            self.finished = True

    async def receive(self, text_data=None, bytes_data=None):
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
                if activeGames[self.room_group_name].gameLoop.game.playing:
                    activeGames[self.room_group_name].gameLoop.game.playing = False
                else:
                    activeGames[self.room_group_name].gameLoop.game.playing = True

            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "websocket.message",
                    "message": data
                }
            )
            if self.finished:
                await self.close(1000)

    async def websocket_message(self, event):
        # This is called when a message is received from the group
        if not self.finished:
            await self.send(text_data=json.dumps(event["message"]))

    async def websocket_accept(self, event):
        print("websocket_accept")
        # Handle WebSocket connection accept event
        await self.send(text_data=json.dumps(event["message"]))

    async def websocket_close(self, event):
        print("websocket_close")
        # Handle WebSocket connection close event
        await self.send(text_data=json.dumps(event["message"]))

# re_path(r'ws/Monitor/Lobby/(?P<lobby_id>[\w-]+)/$', consumers.LobbyConsumer.as_asgi()),
