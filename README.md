# Digital Bank

### Development server
Make sure you have docker installed and running on your machine and then run below command,
```
docker-compose up --build --remove-orphans
```

### Healthcheck
Banking Service - http://127.0.0.1:8000
<br>
Statement Generation Service http://127.0.0.1:8001

### Postman collection
[Banking service](/Banking%20APIs.postman_collection.json)
Get authorization token from authentication API and update in postman collection to access user specific APIs.

### Monthly statement scheduler
Notes:
- Create user(s) before checking logs of this scheduler.
- Note that scheduler runs every 10 sec for demonstration purpose right now. change it with crontab express in future.

### Questions
1)  Please outline the steps you would take to dockerize the application and the Dockerfile(s) you would use.
    - [Dockerization Guide](/dockerization-guide.md)

2)  Please also outline how you would manage configuration variables such as database connection strings and API keys in a production environment
    - **Secrets Management**: Consider using secrets management solutions like HashiCorp Vault or AWS Secrets Manager to securely store and retrieve sensitive data.

    - **Container Orchestration**: For containerized apps, use Kubernetes to securely inject secrets into containers as environment variables or mounted files

    - **Configuration Files**: Use a configuration file (e.g., .env or .ini) to store non-sensitive configuration variables. Libraries like python-decouple or python-dotenv can help read these values from files and environment variables.
