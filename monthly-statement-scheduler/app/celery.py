import os
from celery import Celery

celery_broker_url = os.environ.get('CELERY_BROKER_URL', '')

app = Celery(
    'monthly_statements_generation',
    broker=celery_broker_url,
    include=['app.tasks']
)

if __name__ == '__main__':
    app.start()