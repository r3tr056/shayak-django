from django.contrib import admin
from .models import Feedback
from users.models import User

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'rating', 'date')
    list_filter = ('user', 'content', 'date')
    search_fields = ('user', 'content')

    class Meta:
        model = Feedback

admin.site.register(Feedback, FeedbackAdmin)