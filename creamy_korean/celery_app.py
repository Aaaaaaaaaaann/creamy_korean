import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creamy_korean.settings')

celery_app = Celery('creamy_korean',
                    brocker='amqp://localhost')
celery_app.autodiscover_tasks()
