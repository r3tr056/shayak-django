from django.db import models

class Document(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    compressed_content = models.BinaryField(blank=True)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('NEED_CORRECTION', 'Need Correction'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

