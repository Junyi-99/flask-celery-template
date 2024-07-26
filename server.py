from app.services.async_task import async_task
from app.utils.factory import flask_init_app
from app.views import simple_service

flask_app = flask_init_app()
flask_app.register_blueprint(simple_service)
flask_app.register_blueprint(async_task)

# `celery -A server worker` needs this variable
celery_app = flask_app.extensions["celery"]


@flask_app.after_request
def apply_default_headers(response):
    headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST",
        "Access-Control-Allow-Headers": "Content-Type",
    }
    response.headers.extend(headers)
    return response


if __name__ == "__main__":
    flask_app.run(debug=True)
