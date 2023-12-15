import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from channels.db import database_sync_to_async
from channels.layers import get_channel_layer

from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import DynamicFormData
from .tasks import get_response

class ChatConsumer(WebsocketConsumer):

    async def connect(self):
        user = await self.get_user()
        if not user.is_authenticated:
            await self.close(403)
        else:
            self.user_data = await self.get_user_data(user)
            self.register_action_handlers()
            await self.accept()

    async def disconnect(self, code):
        # TODO : Clean up resources used for the Chat
        pass

    async def get_action(self, json_data):
        action_type = json_data.get('action_type', None)
        return action_type

    async def receive(self, text_data=None, bytes_data=None):
        try:
            data = json.loads(text_data)
        except json.JSONDecodeError as ex:
            # Close with the code 500, Server Error
            await self.close(500)

        user_message = data.get('message')
        ai_response = get_response.delay(self.channel_name, user_message)
        action = await self.get_action(ai_response)

        await self.handle_action(action, ai_response)
    
    def register_action_handlers(self):
        self.action_handlers = {
            "message": self.send_message_to_client,
            "create_document": self.handle_create_document,
            "review_document": self.handle_review_document,
            "notify_event": self.handle_notify_legal_event,
            "search_web": self.handle_search_web,
        }

    async def handle_action(self, action, ai_response):
        handler = self.action_handlers.get(action, self.handle_unknown_action)
        handler(self.channel_name, ai_response)

    async def handle_unknown_action(self):
        pass

    def send_message_to_client(channel_name, ai_response):
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.send)(channel_name, {
            "action_type": "ai_response",
            "message": ai_response,
        })

    @database_sync_to_async
    def get_user(self):
        jwt_token = self.scope.get('query_string').decode('utf-8').split('=')[1]
        auther = JWTAuthentication()
        user, _ = auther.authenticate(self.scope)

        return user
    
    @database_sync_to_async
    def get_user_data(self, user):
        return {'email': user.email}
    

    def get_ai_response(self, user_input):
        pass