import json
#from django.contrib.auth.models import User
from authentication.models import User
from .models import Group
from authentication.models import User
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
import asyncio
from .game_logic import define_winner
from asgiref.sync import async_to_sync
choices_of_players = []

class HomeWebSocket(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add(
            "home", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        user_id = text_data.get("user_id", None)
        inviting_user_id = text_data.get("inviting_user_id", None)

        inviting_user = await database_sync_to_async(User.objects.get)(user_id=inviting_user_id)
        inviting_username = f'{inviting_user.first_name} {inviting_user.last_name}'


        await self.channel_layer.group_send('home', {
            "type": type,
            "user_id": user_id,
            "inviting_username": inviting_username,
            "inviting_user_id": inviting_user_id

        })

    async def invite(self, event):
        type = event['type']
        user_id = event['user_id']
        inviting_username = event['inviting_username']
        inviting_user_id = event['inviting_user_id']

        returned_data = {
            "type": type,
            "user_id": user_id,
            'inviting_username': inviting_username,
            'inviting_user_id': inviting_user_id
        }
        await self.send(json.dumps(
            returned_data
        ))
class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = str(self.scope["url_route"]["kwargs"]["group_id"])

        self.group = await database_sync_to_async(Group.objects.get)(group_id=self.group_id)
        await self.channel_layer.group_add(
            self.group_id, self.channel_name)
        self.user = self.scope["user"]

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        global choices_of_players
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        message = text_data.get("message", None)
        user_id = text_data.get("user_id", None)
        choices_of_players.append({'choice': message, 'user_id': user_id})

        if len(choices_of_players) == 2:
            winner_id = define_winner(choices_of_players)
            await self.channel_layer.group_send(self.group_id, {
                "type": "win_message",
                "winner_id": winner_id,
                "user_id": user_id
            })
        else:
            await self.channel_layer.group_send(self.group_id, {
                "type": type,
                "message": message,
                "user_id": user_id
            })

    async def win_message(self, event):
        winner_id = event["winner_id"]
        user_id = event['user_id']

        returned_data = {
            "type": "win_message",
            "winner_id": winner_id,
            "user_id": user_id
        }
        await self.send(json.dumps(
            returned_data
        ))

    async def choice_message(self, event):
        message = event["message"]
        user_id = event['user_id']

        returned_data = {
            "type": 'choice_message',
            "message": message,
            "user_id": user_id
        }
        await self.send(json.dumps(
            returned_data
        ))

