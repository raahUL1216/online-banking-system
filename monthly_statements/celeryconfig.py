import os
celery_broker_url = os.environ.get('CELERY_BROKER_URL', '')


broker_url = celery_broker_url
task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Kolkata'
enable_utc = True