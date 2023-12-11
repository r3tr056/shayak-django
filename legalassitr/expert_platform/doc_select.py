from django.db.models import Avg
from expert_platform.models import Document, Expert, Feedback

def select_expert_for_document(document_id):
    document = Document.objects.get(pk=document_id)
    
    # Calculate the average response time for each expert
    experts = Expert.objects.annotate(
        avg_response_time=Avg('responses__response_time'),
        avg_user_rating=Avg('feedbacks__rating')
    )
    
    # Sort experts by average response time, time spent on the app, and average user rating
    sorted_experts = sorted(
        experts,
        key=lambda expert: (expert.avg_response_time, expert.time_spent_on_app, -expert.avg_user_rating)
    )
    
    # Select the expert based on the sorting criteria
    selected_expert = sorted_experts[0]
    
    # Assign the selected expert to review the document
    document.expert_reviewer = selected_expert
    document.save()
    
    return selected_expert
