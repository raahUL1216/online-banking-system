from monthly_statements.celery import app

from monthly_statements.database import get_db
from monthly_statements.models import User
from monthly_statements.statement import generate_monthly_statement

from datetime import datetime, timedelta

@app.task
def generate_monthly_statements():
    '''
    Retrieve users and create monthly statement for each user
    '''
    gen_db = get_db()
    db = next(gen_db)
    users = db.query(User).all()
    
    today = datetime.now()
    previous_month = (today.replace(day=1) - timedelta(days=1)).month
    current_year = today.strftime('%Y')

    for user in users:
        generate_monthly_statement(user.id, previous_month, current_year)
