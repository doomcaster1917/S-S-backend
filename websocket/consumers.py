import json
from .models import Group, User
from channels.generic.websocket import WebsocketConsumer, AsyncWebsocketConsumer
from channels.layers import channel_layers
from channels.db import database_sync_to_async
import asyncio
from .game_logic import define_winner
from asgiref.sync import async_to_sync
from .logs import log_parser

choices_of_players = []


class HomeWebSocket(AsyncWebsocketConsumer):
    async def connect(self):

        await self.channel_layer.group_add(
            "home", self.channel_name)
        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):

        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        if type == 'invite':
            user_id = text_data.get("user_id", None)
            inviter_user_id = int(text_data.get("inviter_user_id", None))

            inviter_user = await database_sync_to_async(User.objects.get)(user_id=inviter_user_id)
            inviting_username = f'{inviter_user.first_name} {inviter_user.last_name}'

            await self.channel_layer.group_send('home', {
                "type": type,
                "user_id": user_id,
                "inviter_username": inviting_username,
                "inviter_user_id": inviter_user_id
            })

        elif type == "accept_game":
            print(text_data)
            owner_id = text_data.get('owner_id', None)
            guest_id = text_data.get('guest_id', None)
            self.group = await database_sync_to_async(Group().add_group)(owner_id=owner_id,
                                                                         guest_id=guest_id)

            await self.channel_layer.group_send('home', {
                "type": type,
                "owner_id": owner_id,
                "guest_id": guest_id,
            })

    async def invite(self, event):
        type = event['type']
        user_id = event['user_id']
        inviter_username = event['inviter_username']
        inviter_user_id = event['inviter_user_id']

        returned_data = {
            "type": type,
            "user_id": user_id,
            'inviter_username': inviter_username,
            'inviter_user_id': inviter_user_id
        }
        await self.send(json.dumps(
            returned_data
        ))

    async def accept_game(self, event):
        type = event['type']
        owner_id = event['owner_id']
        guest_id = event['guest_id']

        returned_data = {
            "type": type,
            "owner_id": owner_id,
            'guest_id': guest_id
        }

        await self.send(json.dumps(
            returned_data
        ))


class GroupConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.owner_id = str(self.scope["url_route"]["kwargs"]["owner_id"])

        self.group = await database_sync_to_async(Group.objects.get)(owner_id=self.owner_id)
        await self.channel_layer.group_add(
            self.owner_id, self.channel_name)
        self.user = self.scope["user"]

        await self.accept()

    async def receive(self, text_data=None, bytes_data=None):
        global choices_of_players
        text_data = json.loads(text_data)
        type = text_data.get("type", None)
        message = text_data.get("message", None)
        user_id = text_data.get("user_id", None)
        choices_of_players.append({'choice': message, 'user_id': user_id})

        if len(choices_of_players) > 1:
            winner = define_winner(choices_of_players)

            if isinstance(winner, list):
                await self.channel_layer.group_send(self.owner_id, {
                    "type": "draw_message",
                    "choice": winner[1]
                })
                choices_of_players = []

            else:
                await self.channel_layer.group_send(self.owner_id, {
                    "type": "win_message",
                    "winner_id": winner['winner_id'],
                    "winner_choice": winner['winner_choice'],
                    "looser_choice": winner['looser_choice']
                })
                choices_of_players = []
        else:
            await self.channel_layer.group_send(self.owner_id, {
                "type": type,
                "message": message,
                "user_id": user_id
            })

    async def disconnect(self, code):
        await self.channel_layer.group_send(self.owner_id, {
            "type": "exit",
        })


    async def win_message(self, event):
        type = event['type']
        winner_id = event["winner_id"]
        winner_choice = event['winner_choice']
        looser_choice = event['looser_choice']

        returned_data = {
            "type": type,
            "winner_id": winner_id,
            'winner_choice': winner_choice,
            'looser_choice': looser_choice

        }
        await self.send(json.dumps(
            returned_data
        ))

    async def draw_message(self, event):
        type = event['type']
        choice = event['choice']
        returned_data = {'type': type, 'choice': choice}
        await self.send(json.dumps(
            returned_data
        ))

    async def choice_message(self, event):
        message = event["message"]
        user_id = event['user_id']

        returned_data = {
            "type": 'choice_message',
            "message": message,
            'user_id': user_id
        }
        await self.send(json.dumps(
            returned_data
        ))

    async def exit(self, event):
        global choices_of_players
        type = event["type"]
        returned_data = {
            "type": type,
        }
        await self.send(json.dumps(
            returned_data
        ))

        await self.channel_layer.group_discard(
            self.owner_id,
            self.channel_name
        )
        await self.close()
        await database_sync_to_async(self.group.delete)()
        choices_of_players = []