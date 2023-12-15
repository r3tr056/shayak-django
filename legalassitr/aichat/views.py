from rest_framework import generics
from .models import DynamicFormData
from .serializers import DynamicFormDataSerializer

class DynamicFormListCreateView(generics.ListCreateAPIView):
    queryset = DynamicFormData.objects.all()
    serializer_class = DynamicFormDataSerializer

class DynamicFormRetriveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DynamicFormData.objects.all()
    serializer_class = DynamicFormDataSerializer