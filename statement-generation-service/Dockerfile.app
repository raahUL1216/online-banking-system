# Use an official Python 3.10 image as the base image
FROM python:3.10

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Create a working directory inside the container
WORKDIR /app

# Copy Pipfile and Pipfile.lock into the container's working directory
COPY Pipfile Pipfile.lock /app/

# Install pipenv and project dependencies
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Copy the rest of your application code into the container
COPY . /app/

# Expose the port your statement generation service listens on
EXPOSE 8001

# Specify the command to run your application
CMD ["pipenv", "run", "python", "main.py"]
