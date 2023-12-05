from rest_framework import generics
from .models import Expert
from .serializers import ExpertSerializer

class ExpertListCreateAPIView(generics.ListCreateAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer

class ExpertDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Expert.objects.all()
    serializer_class = ExpertSerializer


# Create your views here.
