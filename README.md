# Flask-Celery Template

| Condition                      | Result                                                                                       |
|--------------------------------|----------------------------------------------------------------------------------------------|
| Flask is shut down             | Does not affect Celery                                                                       |
| Celery is shut down            | Flask receives tasks, but no one executes them, so all tasks remain in Pending status        |
| Flask is running, Celery is not | Tasks are submitted to Redis with status Pending; Celery will execute pending tasks once started |

## Prerequisites

Ensure you have `Python 3.12` installed and a `Redis` instance running.

You can quickly set up a Redis instance using Docker:

```bash
docker run -d --name celery-redis -p 6379:6379 redis
```

## Option I: Manually

Start the Celery worker and the Flask development server with the following commands:

```bash
# Start the Celery worker with INFO level logging
celery -A server worker --loglevel INFO

# Run the Flask development server
flask --app server.flask_app run

# Optional: Start the Celery periodic task scheduler (e.g., for auto-backup)
# celery -A server beat --loglevel INFO

# Optional: Display all routes for the Flask application
# flask --app server routes
```

By following these steps, you will have Flask and Celery running, ready to handle tasks efficiently.

## Option II: Docker

```bash
echo "REDIS_PASSWORD=somerandompassword" > .env
docker compose build

# Start all services
docker compose up

# Stop all services
docker compose down
```
