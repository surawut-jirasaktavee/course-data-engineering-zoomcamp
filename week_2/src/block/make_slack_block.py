# type: ignore
# pylint: disable=missing-module-docstring

from prefect_slack import SlackCredentials  # pylint: disable=import-error
from prefect_slack import SlackWebhook  # pylint: disable=import-error


slack_block = SlackCredentials(token="")
slack_block.save("slack-prefect-bot", overwrite=True)

slack_webhook_block = SlackWebhook(
    url=""
)
slack_webhook_block.save("slack-prefect-webhook-block", overwrite=True)
