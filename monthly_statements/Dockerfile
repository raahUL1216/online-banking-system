# pull official base image
FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app
COPY requirements.txt /app/

# Install project dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# copy project
COPY . /app/

# CMD ["celery", "-A", "monthly_statements", "worker", "--beat", "--loglevel=debug"]