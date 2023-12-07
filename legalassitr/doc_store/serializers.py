from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = '__all__'

class DocumentContentSerializer(serializers.ModelSerializer):
    content = serializers.SerializerMethodField()

    class Meta:
        model = Document
        fields = "__all__"

    def get_content(self, obj):
        return obj.documentcontent.content if hasattr(obj, 'documentcontent') else None
