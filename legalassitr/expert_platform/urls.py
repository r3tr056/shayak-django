from django.urls import path
from .views import ExpertListCreateAPIView, ExpertDetailAPIView
from .import views

urlpatterns = [
    path('experts/', ExpertListCreateAPIView.as_view(), name='expert-list'),
    path('experts/detail/', ExpertDetailAPIView.as_view(), name='expert-detail'),
     path('messages/<int:sender_id>/<int:receiver_id>/', views.GetMessages.as_view(), name='get_messages'),
    path('send/', views.SendMessage.as_view(), name='send_message'),
]
