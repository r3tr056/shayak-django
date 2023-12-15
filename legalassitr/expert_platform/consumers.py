# consumers.py
import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Message
from doc_store.models import Document
from users.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.sender_id = self.scope['url_route']['kwargs']['sender_id']
        self.room_group_name = f'chat_{self.sender_id}'

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
        message_type = text_data_json.get('message_type')
        
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        messeges_pending = Message.objects.filter(sender=sender, receiver=receiver, is_pending=False).exists()

        if receiver.is_expert and not messeges_pending:
            # Prevent the expert from initiating chats
            await self.send(text_data=json.dumps({
                'error': 'Experts cannot initiate chats.'
            }))
        else:
            if message_type == 'text':
                message_content = text_data_json.get('message')
                # Save the message and set it as not pending
                message = Message.objects.create(sender=sender, receiver=receiver, content=message_content, is_pending=False)
                message.save()
                await self.channel_layer.group_send(
                    f'chat_{sender_id}',
                    {
                        'type': 'chat_message',
                        'message_type': 'text',
                        'message': message_content
                    }
                )
            elif message_type == "document":
                doc_id = text_data_json.get('doc_id')
                exists = Document.objects.filter(pk=doc_id).exists()
                if exists:
                    await self.channel_layer.group_send(
                        f'chat_{sender_id}',
                        {
                            'type': 'chat_message',
                            'message_type': 'document',
                            'doc_id': doc_id
                        }
                    )
            elif message_type == "voice":
                voice_content = text_data_json.get('voice_msg')
                voice_note_content = base64.b64decode(voice_content)
                voice_note_message = Message.objects.create(
                    sender=sender, receiver=receiver, content=voice_note_content
                )
                voice_note_message.save()
                down_link = voice_note_message.generate_voice_note_download_link()

                await self.channel_layer.group_send(
                    f'chat_{sender_id}',
                    {
                        'type': 'chat_message',
                        'message_type': 'voice_note',
                        'message': down_link,
                    }
                )

    async def chat_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
