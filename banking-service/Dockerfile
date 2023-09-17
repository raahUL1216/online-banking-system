# Use an official Python 3.10 image as the base image
FROM python:3.10

# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

# Create a working directory
WORKDIR /app
COPY requirements.txt /app/

# Install project dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

# Copy the rest of your application code into the container
COPY . /app/

# Expose the port your banking service listens on (if applicable)
EXPOSE 8000

# Specify the command to run your application
CMD ["python", "main.py"]