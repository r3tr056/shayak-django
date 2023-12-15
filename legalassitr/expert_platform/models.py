import os
import base64

from django.db import models
from django.db.models import Avg
from django.conf import settings

from doc_store.models import Document
from users.models import User

def voice_note_file_path(instance, filename):
    user_id = instance.sender.id
    timestamp = instance.timestamp.strftime('%Y%m%d_%H%M%S')
    return f'voice_notes/user_{user_id}/{timestamp}_{filename}'

class Expert(User, models.Model):
    name = models.CharField(max_length=100)
    time_spent_on_app = models.IntegerField(default=0)
    assigned_docs = models.ManyToManyField(Document)

    def calculate_avg_response_time(self):
        return self.responses.aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0

    def calculate_avg_user_rating(self):
        return self.feedbacks.aggregate(avg_user_rating=Avg('rating'))['avg_user_rating'] or 0


class Response(models.Model):
    expert = models.ForeignKey(Expert, related_name='responses', on_delete=models.CASCADE)
    response_time = models.FloatField()

class Feedback(models.Model):
    expert = models.ForeignKey(Expert, related_name='feedbacks', on_delete=models.CASCADE)
    rating = models.IntegerField()
    # Other feedback-related fields if needed

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_pending = models.BooleanField(default=True)

    TEXT = 'text'
    DOCUMENT = 'document'
    VOICE_NOTE = 'voice_note'

    MESSAGE_TYPES = [
        (TEXT, 'text'),
        (DOCUMENT, 'document'),
        (VOICE_NOTE, 'voice_note')
    ]

    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default=TEXT)

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content}'
    
    def generate_voice_note_download_link(self):
        if self.message_type == self.VOICE_NOTE:
            if not self.content:
                return None
            
            voice_note_dir = os.path.join(settings.MEDIA_ROOT, 'voice_notes')
            os.makedirs(voice_note_dir)

            # generate a unique filename for each voice note
            voice_note_filename = f"{self.timestamp.strftime('%Y%m%d_%H%M%S')}_{self.sender.email}.ogg"
            voice_note_path = os.path.join(voice_note_dir, voice_note_filename)

            with open(voice_note_path, 'wb') as voice_note_file:
                voice_note_file.write(base64.b64decode(self.content))

            download_link = os.path.join(settings.MEDIA_URL, 'voice_notes', voice_note_filename)

            # generate the download link
            download_link = os.path.join(settings.MEDIA_URL, 'voice_notes', voice_note_filename)
            return download_link
        
        return None
    
            