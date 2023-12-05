from rest_framework import serializers
from .models import Expert

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
