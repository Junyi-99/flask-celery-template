from celery import Celery, Task
from flask import Flask


def celery_init_app(flask_app: Flask) -> Celery:
    class FlaskTask(Task):
        def __call__(self, *args: object, **kwargs: object) -> object:
            with flask_app.app_context():
                return self.run(*args, **kwargs)

    celery_app = Celery(flask_app.name, task_cls=FlaskTask)
    celery_app.config_from_object(flask_app.config["CELERY"])
    celery_app.set_default()
    flask_app.extensions["celery"] = celery_app
    return celery_app


def flask_init_app() -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_mapping(
        CELERY=dict(
            broker_url="redis://localhost:6379/0",
            broker_connection_retry_on_startup=True,
            result_backend="redis://localhost:6379/0",
            task_serializer="json",
            task_ignore_result=False,
            task_track_started=True,
            accept_content=["json"],
            result_serializer="json",
        )
    )
    flask_app.config.from_prefixed_env()
    return flask_app
