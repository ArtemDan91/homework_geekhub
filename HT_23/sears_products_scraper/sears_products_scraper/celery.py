import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sears_products_scraper.settings')

app = Celery('sears_products_scraper')

app.conf.broker_connection_retry_on_startup = True

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')