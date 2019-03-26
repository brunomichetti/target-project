from channels.generic.websocket import AsyncWebsocketConsumer
import json
import datetime

from chat.models import MatchMessage
from targets.models import Match
from targets.signals import send_msg_notification_to_users
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

        match_msg = MatchMessage(
            in_match=self.match,
            content=message,
            sent_by=self.user
        )
        match_msg.save()
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'msg_id': match_msg.id,
                'message': message,
                'user_id': self.user.id,
                'user_name': self.user.name
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        if event['user_id'] == self.user.id:
            if (self.channel_layer.receive_count == 0):
                if (self.match.target_1.user_id != self.user.id):
                    other_user_id = self.match.target_1.user_id
                else:
                    other_user_id = self.match.target_2.user_id
                send_msg_notification_to_users(
                    event['user_name'],
                    other_user_id,
                    message,
                    datetime.datetime.now()
                )
            message = 'You : ' f'{message}'
        else:
            MatchMessage.objects.filter(id=event['msg_id']).update(
                seen_at=datetime.datetime.now()
            )
            message = f"{event['user_name']}" " : " f"{message}"
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
