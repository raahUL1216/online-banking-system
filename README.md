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

### Questions
1)  Please outline the steps you would take to dockerize the application and the Dockerfile(s) you would use.
    - [Dockerization Guide](/dockerization-guide.md)

2)  Please also outline how you would manage configuration variables such as database connection strings and API keys in a production environment
    - **Environment Variables**: Store sensitive information like database connection strings and API keys as environment variables on the production server. Python's os module can be used to access these variables.

    - **Configuration Files**: Use a configuration file (e.g., .env or .ini) to store non-sensitive configuration variables. Libraries like python-decouple or python-dotenv can help read these values from files and environment variables.

    - **Secrets Management**: For more advanced security, consider using secrets management solutions like HashiCorp Vault or AWS Secrets Manager to securely store and retrieve sensitive data.