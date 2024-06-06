from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ssms_project.settings')

app = Celery('ssms_project')

app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




# 1. Start Celery Beat:
  # Start the Celery Beat scheduler to activate the periodic task:
  # celery -A ssms_project.celery beat --loglevel=info         run this command


# 2. Start Celery Worker
  # To execute the periodic task, start the Celery worker:

  # celery -A ssms_project worker -l INFO 

# NB: keep both the Celery worker and Celery Beat scheduler running simultaneously for the periodic task to work correctly.