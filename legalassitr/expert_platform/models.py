from django.db import models
from django.db.models import Avg
from doc_store.models import Document
from auth.models import User


class Expert(User):
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

    def __str__(self):
        return f'{self.sender} -> {self.receiver}: {self.content}'