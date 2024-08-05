import os

from flask import Blueprint

from app.blueprints.file_upload import UPLOAD_PATH
from app.tasks.simple_task import send_email

file_process = Blueprint(
    name="file_process_service",
    import_name=__name__,
    url_prefix="/file/process",
    template_folder="../templates/file_process",
)


@file_process.route("/<filename>", methods=["GET"])
def file_process_fn(filename: str):
    """
    Using celery task to handle the uploaded file (by file_upload.py)
    """
    # filename = request.args.get("filename", type=str)
    if filename is None or filename == "":
        return {"error": "No `filename` provided"}, 400

    file_path = os.path.join(UPLOAD_PATH, filename)

    result = send_email.delay(file_path)
    return {"task_id": result.id}
