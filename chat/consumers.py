from channels.generic.websocket import AsyncWebsocketConsumer
import json

from chat.models import MatchMessage
from targets.models import Match
from users.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.user = self.scope['user']
        if '_wrapped' in self.user.__dict__:
            self.user = self.user._wrapped
        self.match = Match.objects.get(
            pk=self.scope['url_route']['kwargs']['match_id']
        )
        self.room_group_name = 'chat_' f'{self.match.id}'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        new_msg = MatchMessage(
            in_match=self.match,
            content=message,
            sent_by=self.user
        )
        new_msg.save()

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user_id': self.user.id,
                'user_name': self.user.name
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        if event['user_id'] == self.user.id:
            message = 'You : ' f'{message}'
        else:
            message = f"{event['user_name']}" " : " f"{message}"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
