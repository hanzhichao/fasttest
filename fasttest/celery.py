import os

from celery import Celery

PROJECT_NAME = os.path.basename(os.path.dirname(__file__))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', f'{PROJECT_NAME}.settings')

app = Celery(PROJECT_NAME)

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()
