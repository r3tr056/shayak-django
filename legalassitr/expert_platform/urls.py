from django.urls import path
from .views import ExpertListCreateAPIView, ExpertDetailAPIView

urlpatterns = [
    path('experts/', ExpertListCreateAPIView.as_view(), name='expert-list'),
    path('experts/detail/', ExpertDetailAPIView.as_view(), name='expert-detail'),
]
