from celery import app
from app.tasks import generate_monthly_statements
from celery.schedules import crontab

# Generate monthly statement for all users on the 1st day of every month
app.conf.beat_schedule = {
    'generate-monthly-statements': {
        'task': 'app.tasks.generate_monthly_statements',
        'schedule': crontab(day_of_month=1),
    },
}

if __name__ == '__main__':
    app.start()