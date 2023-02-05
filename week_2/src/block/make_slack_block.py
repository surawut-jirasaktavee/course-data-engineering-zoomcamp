# type: ignore
# pylint: disable=missing-module-docstring

from prefect_slack import SlackCredentials  # pylint: disable=import-error
from prefect_slack import SlackWebhook  # pylint: disable=import-error


slack_block = SlackCredentials(token="dd5c3cbefa87faf74d6722f62c859805")
slack_block.save("slack-prefect-bot", overwrite=True)

slack_webhook_block = SlackWebhook(
    url="https://hooks.slack.com/services/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"
)
slack_webhook_block.save("slack-prefect-webhook-block", overwrite=True)
