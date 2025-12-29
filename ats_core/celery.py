import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ats_core.settings')

app = Celery('ats_core')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
