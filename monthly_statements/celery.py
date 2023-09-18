import os
from celery import Celery
from celery.schedules import crontab

celery_broker_url = os.environ.get('CELERY_BROKER_URL', '')

app = Celery(
    'monthly_statements',
    broker=celery_broker_url
)

# Generate monthly statement for all users on the 1st day of every month
app.conf.beat_schedule = {
    'generate-monthly-statements': {
        'task': 'monthly_statements.tasks.generate_monthly_statements',
        'schedule': crontab(minute='*')
    },  
}

if __name__ == '__main__':
    app.start()
