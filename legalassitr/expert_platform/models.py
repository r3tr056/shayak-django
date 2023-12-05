from django.db import models
from django.db.models import Avg
from doc_store.models import Document


class Expert(models.Model):
    name = models.CharField(max_length=100)
    time_spent_on_app = models.IntegerField(default=0)

    def calculate_avg_response_time(self):
        return self.responses.aggregate(avg_response_time=Avg('response_time'))['avg_response_time'] or 0

    def calculate_avg_user_rating(self):
        return self.feedbacks.aggregate(avg_user_rating=Avg('rating'))['avg_user_rating'] or 0

    def select_expert_for_document(self, document_id):
        
        document = Document.objects.get(pk=document_id)
        
        # Calculate the average response time for the expert
        avg_response_time = self.calculate_avg_response_time()
        
        # Calculate the average user rating for the expert
        avg_user_rating = self.calculate_avg_user_rating()
        
        # Assign the expert to review the document
        document.expert_reviewer = self
        document.save()
        
        return {
            'expert_id': self.id,
            'expert_name': self.name,
            'avg_response_time': avg_response_time,
            'avg_user_rating': avg_user_rating
        }

class Response(models.Model):
    expert = models.ForeignKey(Expert, related_name='responses', on_delete=models.CASCADE)
    response_time = models.FloatField()

class Feedback(models.Model):
    expert = models.ForeignKey(Expert, related_name='feedbacks', on_delete=models.CASCADE)
    rating = models.IntegerField()
    # Other feedback-related fields if needed
