from django.contrib import admin
from aichat.models import Conversation, DynamicForm, Message, UploadDocument

# Register your models here.
admin.site.register(UploadDocument)
admin.site.register(Conversation)
admin.site.register(Message)
admin.site.register(DynamicForm)