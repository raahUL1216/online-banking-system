from celery import shared_task

from app.database import get_db
from app.models import User
from app.statement import generate_monthly_statement

from datetime import datetime, timedelta

db = get_db()

@shared_task
def generate_monthly_statements():
    '''
    Retrieve users and create monthly statement for each user
    '''
    users = User.query.all()
    
    today = datetime.now()
    previous_month = (today.replace(day=1) - timedelta(days=1)).strftime('%B')
    current_year = today.strftime('%Y')

    for user in users:
        generate_monthly_statement(user.user_id, previous_month, current_year)
