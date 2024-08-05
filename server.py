from app.blueprints.file_process import file_process

# Demo for file upload and long running process
from app.blueprints.file_upload import file_upload
from app.blueprints.simple_service import simple_service
from app.blueprints.task_result import task_result
from app.utils.factory import celery_init_app, flask_init_app

flask_app = flask_init_app()
flask_app.register_blueprint(simple_service)
flask_app.register_blueprint(task_result)
flask_app.register_blueprint(file_upload)
flask_app.register_blueprint(file_process)

# `celery -A server worker` needs this variable
celery_app = celery_init_app(flask_app)


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
