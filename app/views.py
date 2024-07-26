from flask import Blueprint, render_template, request

from app.tasks import add_together, send_email

simple_service = Blueprint(
    name="simple_service",
    import_name=__name__,
    template_folder="templates/simple_service",
)


@simple_service.route("/add")
def start_add() -> dict[str, object]:
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    result = add_together.delay(a, b)
    return {"task_id": result.id}


@simple_service.route("/send_email")
def start_send_email() -> dict[str, object]:
    result = send_email.delay()
    return {"task_id": result.id}


@simple_service.route("/")
def hello_world():
    return render_template("index.html", name="User")
