from django.urls import path
from .views import FeedbackListCreateView, FeedbackRetriveUpdateDestroyView

urlpatterns = [
    path('feedback/', FeedbackListCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/', FeedbackRetriveUpdateDestroyView.as_view(), name='feedback_detail')
]