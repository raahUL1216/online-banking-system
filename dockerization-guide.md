# Dockerization Guide

This guide outlines the steps to Dockerize banking-service for easy deployment and management. Docker allows you to package your application and its dependencies into a single, portable container.

## Prerequisites

Before you begin, ensure that you have the following installed on your system:

- Docker: [Install Docker](https://docs.docker.com/get-docker/)
- Docker Compose (optional): [Install Docker Compose](https://docs.docker.com/compose/install/)

## Dockerization Steps

1. **Create Dockerfile**:
   - Create a `Dockerfile.app` in the root of your project directory.
   - Use an official Python 3.10 image as the base image.
   - Specify the working directory (`WORKDIR`) inside the container.
   - Copy `Pipfile` and `Pipfile.lock` into the container's working directory.
   - Install `pipenv` and project dependencies using the following commands:
     ```bash
     RUN pip install pipenv
     RUN pipenv install --deploy --ignore-pipfile
     ```
   - Copy the rest of your application code into the container.
   - Expose port 8000 (or the port your banking service listens on).
   - Specify the command to run your application:
     ```bash
     CMD ["pipenv", "run", "python", "main.py"]
     ```

2. **Create Docker Compose File**:
   - If application depends on other services (e.g., databases), create a `docker-compose.yml` file to define every application with their environment
   - Configure services, networks, volumes, and environment variables in the docker-compose file.

3. **Build the Docker Image**:
   - Open a terminal in the project directory.
   - Run the following command to build the Docker image:
     ```bash
     docker-compose build
     ```

4. **Run the Docker Container**:
   - To run your application in a Docker container, use the following command:
     ```bash
     docker-compose up
     ```
   - Replace `8000:8000` with the desired port mapping.

5. **Access Your Application**:
   - Once the container is running, your application should be accessible in your web browser at `http://localhost:8000` (or the specified port).

6. **Cleanup**:
   - To stop and remove the container, press `Ctrl+C` in the terminal where the container is running.
   - To remove the Docker image, use the following command:
     ```bash
     docker-compose down
     ```