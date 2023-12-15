
from rest_framework import serializers
from .models import DynamicFormData

class DynamicFormDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = DynamicFormData
        fields = ['id', 'form_name', 'form_data']

    