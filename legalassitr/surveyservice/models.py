from django.db import models

from legalassitr.surveyservice.tasks.sentiment import analyze_sentiment

class Feedback(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    content = models.TextField()
    sentiment = models.CharField()
    rating = models.IntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.firstname} - Rating: {self.rating}"
    
    def analyze_sentiment(self):
        self.sentiment = analyze_sentiment.delay(self.content)
        self.save()
        return self.sentiment