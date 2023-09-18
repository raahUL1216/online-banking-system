# Dockerization Guide

This guide outlines the steps to Dockerize banking-service for easy deployment and management. Docker allows you to package your application and its dependencies into a single, portable container.

## Prerequisites

Before you begin, ensure that you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose (optional): [Install Docker Compose](https://docs.docker.com/compose/install/)

## Dockerization Steps

1. **Create Dockerfile**:
   - Create a `Dockerfile` for each service (or app) in your project.

   Example:
   - Use an official Python 3.10 image as the base image.
   - Specify the working directory (`WORKDIR`) inside the container.
   - Copy `requirements.txt` into the container's working directory. So, dependency installation step can be cached with docker.
   - Install dependencies:
     ```bash
     RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
     ```
   - Copy the rest of your application code into the container.
   - Expose port 8000 (or the port your service listens on).
   - Specify the command to run your application:
     ```bash
     CMD ["python", "main.py"]
     ```

2. **Create Docker Compose File**:
   - If application depends on other services (e.g., databases), create a `docker-compose.yml` file to define every application with their environment
   - Configure services, dependencies, volumes, and environment variables in the docker-compose file.

3. **Build and Run the Docker Image**:
   - Open a terminal in the root directory (docker-compose.yaml location).
   - Run the following command to build the Docker image:
     ```bash
     docker-compose up --build -d
     # -d stands for detached mode so container will run in background

     #Seperate command
     docker-compose build
     docker-compose up
     ```

4. **Access Your Application**:
   - Once the container is running, verify that application is accessible, 
      - Check healthcheck endpoint for services.
      - Check container logs for scheduler

5. **Cleanup**:
   - To remove the Docker image, use the following command:
     ```bash
     docker-compose down
     ```