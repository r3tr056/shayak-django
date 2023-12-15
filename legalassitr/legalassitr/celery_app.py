from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'legalassitr.settings')

# Create a celery instance and config it using the django settings
app = Celery('legalassitr')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto discover tasks in all installed apps
app.autodiscover_tasks()
