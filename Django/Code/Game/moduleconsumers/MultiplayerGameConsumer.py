from ctypes.wintypes import POINT

from Game.Game import GameInstance, activeGames, aiGames
from Game.models import Game as GameModel

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

import json

class MultiplayerGameConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_group_name = None
        self.created = False
        self.finished = False


    async def get_game_id(self):
        print(type(self.scope['url_route']['kwargs']['game_id']))
        return self.scope['url_route']['kwargs']['game_id']


    async def get_user_dict(self) -> dict:
        return await sync_to_async(self.scope["user"].getDict)()


    async def get_game_dict(self) -> dict:
        game_model = await sync_to_async(GameModel.objects.filter)(id=self.room_group_name)
        game_model = await sync_to_async(game_model.get)()
        return await sync_to_async(game_model.get)()


    async def get_user_code(self) -> int:
        user_dictionary = await self.get_user_dict()
        return user_dictionary["code"]


    async def send_message(self, event: dict) -> None:
        await self.send(text_data=json.dumps(event["message"]))


    async def create_game_instance(self) -> GameInstance:
        game_dict: dict = await self.get_game_dict()
        player_one_dict: dict = game_dict["PlayerOne"]
        player_two_dict: dict = game_dict["PlayerTwo"]

        player_one_code: int = player_one_dict["Info"]["userCode"]
        player_two_code: int = player_two_dict["Info"]["userCode"]
        player_one_name: str = player_one_dict["Info"]["first_name"]
        player_two_name: str = player_two_dict["Info"]["first_name"]

        return GameInstance(player_one_code, player_two_code, player_one_name, player_two_name)


    async def connect(self):
        if self.scope["user"].is_anonymous:
            await self.close()
        else:
            game_id = self.get_game_id()
            self.room_group_name = 'MultiplayerGame_' + str(game_id)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()

            if not self.created:
                activeGames[self.room_group_name] = self.create_game_instance()
                self.created = True

            await self.channel_layer.group_add({
                "type": "send.message",
                "message": "You are now connected!"
            })


    async def disconnect(self, close_code: int):
        try: # todo -> is this even fair?
            if activeGames[self.room_group_name]:
                del activeGames[self.room_group_name]
        except KeyError:
            print("Error: ", self.room_group_name, "game not found")

        # remove websocket connection from the group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        # todo -> is this needed?
        if not self.finished:
            # todo -> maybe use some sort of pattern here (like a hash map)
            if data["action"] == "paddle-move-notification":

