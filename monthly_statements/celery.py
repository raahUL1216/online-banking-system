from celery import Celery
from celery.schedules import crontab

app = Celery(
    'monthly_statements',
    include=['monthly_statements.tasks']
    )
app.config_from_object('monthly_statements.celeryconfig')


app.conf.beat_schedule = {
    "run-me-every-ten-seconds": {
        "task": "monthly_statements.tasks.generate_monthly_statements",
        "schedule": crontab(minute=1)
    }
}
