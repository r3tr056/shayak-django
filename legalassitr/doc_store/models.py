import zlib

from django.db import models

from users.models import User
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,  related_name='document_user')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    content_summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deltas = models.JSONField(default=list)
    # used to store the chat summary during generation
    gen_summary = models.TextField()

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('NEED_CORRECTION', 'Need Correction'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

class AIIntermediateDoc(models.Model):
    simple_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()