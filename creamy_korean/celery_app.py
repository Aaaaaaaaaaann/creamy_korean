import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'creamy_korean.settings')

celery_app = Celery('creamy_korean',
                    brocker='amqp://localhost')

celery_app.conf.update(worker_max_tasks_per_child=1,
                       broker_pool_limit=None)

celery_app.autodiscover_tasks()
