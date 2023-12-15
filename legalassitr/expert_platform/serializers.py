from rest_framework import serializers

from .models import Expert, Message
from .doc_select import select_expert_for_document
from doc_store.models import Document

class ExpertSerializer(serializers.ModelSerializer):
    avg_response_time = serializers.SerializerMethodField()
    avg_user_rating = serializers.SerializerMethodField()

    class Meta:
        model = Expert
        fields = ('id', 'name', 'time_spent_on_app', 'avg_response_time', 'avg_user_rating')

    def get_avg_response_time(self, obj):
        return obj.calculate_avg_response_time()

    def get_avg_user_rating(self, obj):
        return obj.calculate_avg_user_rating()

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'

class SubmitForExpertReviewSerializer(serializers.ModelSerializer):
    doc_id = serializers.IntegerField()
    expert_id = serializers.IntegerField()

    def validate_doc_id(self, value):
        try:
            document = Document.objects.get(pk=value)
        except Document.DoesNotExist:
            raise serializers.ValidationError(f"Document with id : {value} does not exist.")
        return document
    
    def validate_expert_id(self, value):
        if value is not None:
            try:
                expert = Expert.objects.get(pk=value)
            except Expert.DoesNotExist:
                raise serializers.ValidationError(f"Expert with id : {value} does not exist.")
            return expert
        return None
    
    def validate(self, data):
        doc_id = data.get('doc_id')
        expert_id = data.get('expert_id')

        if expert_id is None:
            selected_expert = select_expert_for_document(doc_id)
        else:
            selected_expert = data['expert_id']

        return {
            'doc_id': doc_id,
            'selected_expert': selected_expert
        }