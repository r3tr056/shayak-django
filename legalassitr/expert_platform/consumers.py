# consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message
from auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        # TODO : Add the started room chat to the expert's profile

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        sender_id = text_data_json.get('sender_id')
        receiver_id = text_data_json.get('receiver_id')
        message_content = text_data_json.get('message')

        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        if receiver.is_expert and not Message.objects.filter(sender=sender, receiver=receiver, is_pending=False).exists():
            # Prevent the expert from initiating chats
            await self.send(text_data=json.dumps({
                'error': 'Experts cannot initiate chats.'
            }))
        else:
            # Save the message and set it as not pending
            message = Message.objects.create(sender=sender, receiver=receiver, content=message_content, is_pending=False)
            message.save()
            await self.channel_layer.group_send(
                f'chat_{sender_id}',
                {
                    'type': 'chat_message',
                    'message': message_content
                }
            )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
