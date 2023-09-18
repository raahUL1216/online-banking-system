from celery import Celery
from celery.schedules import crontab

app = Celery(
    'monthly_statements',
    include=['monthly_statements.tasks']
    )
app.config_from_object('monthly_statements.celeryconfig')


# Generate monthly statement for all users periodically (10 sec for demonstration purpose)
# change "schedule" key with: crontab(day_of_month=1, minute=0, hour=0) to run it 1st day of month

app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "monthly_statements.tasks.generate_monthly_statements",
        "schedule": 10 
    }
}
