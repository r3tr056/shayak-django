from django.core.management.base import BaseCommand

class ChatTrainCommand(BaseCommand):
    help = 'Train the AI for chat'

    def handle(self, *args, **kwargs):
        pass