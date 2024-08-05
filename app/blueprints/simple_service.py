from collections import defaultdict

from flask import Blueprint, current_app, render_template, request

from app.tasks.simple_task import add_together, send_email

simple_service = Blueprint(
    name="simple_service",
    import_name=__name__,
    template_folder="../templates/simple_service",
)


@simple_service.route("/add")
def start_add() -> dict[str, object]:
    """
    An endpoint to demonstrate the simple long-running task
    """
    a = request.args.get("a", type=int)
    b = request.args.get("b", type=int)
    result = add_together.delay(a, b)
    return {"task_id": result.id}


@simple_service.route("/send_email")
def start_send_email() -> dict[str, object]:
    """
    An endpoint to demonstrate the multi-stage task
    """
    result = send_email.delay()
    return {"task_id": result.id}


@simple_service.route("/")
def hello_world():
    # get all routes
    routes = defaultdict(list)
    for rule in current_app.url_map.iter_rules():
        bpname = rule.endpoint.split(".")[0]
        routes[bpname].append((rule.rule, rule.methods))
    return render_template("index.html", name="User", routes=routes)
