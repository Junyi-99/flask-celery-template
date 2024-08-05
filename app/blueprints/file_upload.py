import os
from hashlib import md5
from pathlib import Path
from secrets import token_hex

from flask import Blueprint, render_template, request
from flask_cors import cross_origin

file_upload = Blueprint(
    name="file_upload_service",
    import_name=__name__,
    url_prefix="/file/upload",
    template_folder="../templates/file_upload",
)

UPLOAD_PATH = "uploads"
SUPPORTED_EXTNSIONS = {".txt", ".pdf", ".png", ".jpg", ".jpeg", ".gif"}


@file_upload.route("/", methods=["POST", "OPTIONS"])
@cross_origin()
def file_upload_fn():
    """
    Files uploaded through this endpoint will be placed into `UPLOAD_PATH/`

    and will return a JSON response `{"filename":"uploaded_filename"}`

    You can use this path to access the uploaded files
    """
    upload_file = request.files.get("file")

    if upload_file is None:
        return "No file uploaded", 400

    if upload_file.filename == "":
        return "No file selected", 400

    os.makedirs(UPLOAD_PATH, exist_ok=True)

    file_ext = Path(upload_file.filename).suffix
    if file_ext not in SUPPORTED_EXTNSIONS:
        return f"Invalid file type, supported types are {SUPPORTED_EXTNSIONS}", 400  # noqa: E501

    # Hash the file name by MD5 then append a random string to it to prevent conflicts  # noqa: E501
    md5_filename = md5(upload_file.filename.encode()).hexdigest()
    new_filename = f"{md5_filename}_{token_hex(16)}{file_ext}"
    new_filepath = os.path.join(UPLOAD_PATH, new_filename)
    upload_file.save(new_filepath)

    return {"filename": new_filename}, 200


@file_upload.get("/ui")
def file_upload_ui():
    return render_template("ui.html")


@file_upload.errorhandler(413)
def error_too_large(e):
    return "File is too large", 413
