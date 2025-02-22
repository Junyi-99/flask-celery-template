import logging
import time

from celery import shared_task

from app.blueprints.task_result import progress_callback


@shared_task(ignore_result=False)
def add_together(a: int, b: int) -> int:
    result = a + b
    time.sleep(10)  # Some long running task
    return result


@shared_task(ignore_result=False, bind=True)
def send_email(self, attachment: str | None = None) -> str:
    # Before calling the function, the task status should be "PENDING"
    recipients = [
        "John",
        "Jane",
        "Alice",
        "Bob",
    ]
    totaln = len(recipients)

    # The task status will be updated to "STARTED" by celery automatically
    logging.info(f"Start sending email, with attachment: {attachment}")

    time.sleep(10)

    for idx, rep in enumerate(recipients):
        time.sleep(5)
        logging.info(f"[{idx}/{totaln}] Sending email to {rep} with attachment {attachment})")  # noqa: E501
        # Update the task status to "PROGRESS"
        progress_callback(self, idx + 1, totaln, message=f"Sent to recipient: {rep}")  # noqa: E501

    time.sleep(5)  # final checks...

    # After the return, the task status will be updated to "SUCCESS"
    return f"Email all sent, with attachment: {attachment}"
