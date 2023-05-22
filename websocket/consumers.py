import json
#from django.contrib.auth.models import User
from authentication.models import User
from .models import Event, Message, Group
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
import asyncio
import game_logic
choices_of_players = []

class JoinAndLeave(WebsocketConsumer):

    def connect(self):
        self.user = self.scope["user"]
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type:
            data = text_data.get("data", None)

            if type == "leave_group":
                self.leave_group(data)
            elif type == "join_group":
                self.join_group(data)

    def leave_group(self, group_id):
        group = Group.objects.get(group_id=group_id)
        group.remove_user_from_group(self.user)
        data = {
            "type": "leave_group",
            "data": group_id
        }
        self.send(json.dumps(data))

    def join_group(self, group_id):
        group = Group.objects.get(group_id=group_id)
        group.add_user_to_group(self.user)
        data = {
            "type": "join_group",
            "data": group_id
        }
        self.send(json.dumps(data))


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
            winner_id = game_logic.define_winner(choices_of_players)
            await self.channel_layer.group_send(self.group_id, {
                "type": "End_of_round",
                "message": winner_id,
                "user_id": user_id
            })

        await self.channel_layer.group_send(self.group_id, {
            "type": type,
            "message": message,
            "user_id": user_id
        })

    async def win_message(self, event):

        ...

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

    async def event_message(self, event):
        message = event.get("message")
        user = event.get("user", None)

        await self.send(
            json.dumps(
                {
                    "type": "event_message",
                    "message": message,
                    "status": event.get("status", None),
                    "user": user
                }
            )
        )