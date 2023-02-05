# type: ignore
# pylint: disable=missing-module-docstring

from prefect import flow, task # pylint: disable=import-error
from prefect_slack import SlackWebhook # pylint: disable=import-error


@task(name="Slack_Notification")
def send_message():

    """
    Send message when the flow and sub task is complete
    """

    slack_webhook_block = SlackWebhook.load("slack-prefect-webhook-block")
    slack_webhook_block.notify(
        subject="Flow status of web to gcs", body="Hello from Prefect"
    )


@flow(name="Test noti")
def send_noti():

    """
    Test send notification to Slack app
    """
    send_message()


send_noti()
