from typing import Optional, TypedDict

from celery import Task
from celery.result import AsyncResult
from flask import Blueprint, current_app, jsonify

task_result = Blueprint("task_result", __name__)


class TaskResult(TypedDict):
    ready: bool
    state: str
    current: int
    total: int
    message: str
    result: Optional[object]


def progress_callback(self: Task, current: int, total: int, message: str = "") -> None:  # noqa: E501
    """
    This function is a useful wrapper to update the task state.
    (To prevent you forget some fields)

    **Remember** to set `shared_task(bind=True)` in a celery task
    """
    self.update_state(
        state="PROGRESS",
        meta={"current": current, "total": total, "message": message},
    )


@task_result.get("/task/<task_id>")
def task_result_fn(task_id: str):
    result = AsyncResult(task_id)

    response = TaskResult(ready=result.ready(), state=result.state)  # type: ignore  # noqa: E501

    match result.state:
        case "PENDING":
            response.update({"message": "Task is waiting to be processed."})
        case "STARTED":
            response.update({"message": "Task was started, please wait for the progress update or the final result."})  # noqa: E501
        case "FAILURE":  # eventual state
            response.update({"message": str(result.info)})
        case "SUCCESS":  # eventual state
            response.update({"result": result.result})
        case "PROGRESS":  # Custom progress state
            response.update(
                {
                    "current": result.info["current"],
                    "total": result.info["total"],
                    "message": result.info["message"],
                }
            )  # noqa: E501
        case _:  # catch-all
            response.update({"message": f"Unknown state: {result.state}, info: {result.info}"})  # noqa: E501
    return (jsonify(response), 200)


@task_result.get("/task/all")
def task_result_all_fn():
    celery_app = current_app.extensions["celery"]
    i = celery_app.control.inspect()
    response = {
        "active": i.active(),
        "scheduled": i.scheduled(),
        "reserved": i.reserved(),
        "stats": i.stats(),
    }
    return (jsonify(response), 200)
