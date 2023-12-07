import zlib

from django.db import models
from django.core.files.base import ContentFile

from users.models import User
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_user')
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='documents/')
    compressed_content = models.FileField(upload_to='compressed_docs/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deltas = models.JSONField(default=list)

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('VERIFIED', 'Verified'),
        ('NEED_CORRECTION', 'Need Correction'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')

    def compress_content(self):
        """ Compress the content of the document and saves it """
        if not self.file:
            raise ValueError("Cannot compress content. File is missing")
        
        with self.file.open(mode='rb') as file_content:
            uncomp_data = file_content.read()

        comp_data = zlib.compress(uncomp_data)
        
        compressed_file_content = ContentFile(comp_data)
        self.compress_content.save(f'compressed_{self.title}.gz', compressed_file_content, save=True)

    def decompress_content(self):
        """ Decompress the content of the document in the`compressed_content`"""
        if not self.compressed_content:
            raise ValueError("Cannot decompress content. Compressed content is missing.")
        
        with self.compressed_content.open(mode='rb') as compressd_file:
            compressed_data = compressd_file.read()

        uncompressed_data = zlib.decompress(compressed_data)
        return uncompressed_data

class AIIntermediateDoc(models.Model):
    simple_id = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()