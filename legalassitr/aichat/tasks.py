
from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

@shared_task
def get_response(channel_name, input_data):
    pass