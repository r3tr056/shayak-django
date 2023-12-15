from django.urls import re_path, path

from .consumer import *

websocket_urlpatterns = [
    re_path(r"ws/aichat/$", ChatConsumer.as_asgi())
]