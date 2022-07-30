import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pokecrawler.settings')

BROKER_URL = 'redis://redis:6379/0'
BACKEND_URL = 'redis://redis:6379/1'
app = Celery('pokecrawler', broker=BROKER_URL, backend=BACKEND_URL)

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()