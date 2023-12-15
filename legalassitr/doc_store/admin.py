from django.contrib import admin
from .models import AIIntermediateDoc, Document

# Register your models here.
admin.site.register(Document)
admin.site.register(AIIntermediateDoc)