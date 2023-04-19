from slack_bolt import App
from methods import get_correct_prs
import os

# Install the Slack app and get xoxb- token in advance
slack_bot_token = os.environ['REMIND_SLACK_BOT_TOKEN']
channel_id = os.environ['REMIND_SLACK_CHANNEL']

app = App(token=slack_bot_token)

def main(event, context):
    prs = get_correct_prs()

    if len(prs) == 1:
        app.client.chat_postMessage(channel=channel_id, text='*There is a pull request that can be done:*')
        for pr in prs:
            app.client.chat_postMessage(channel=channel_id, text=pr)

    if len(prs) > 1:
        app.client.chat_postMessage(channel=channel_id, text='*Some code reviews can be done:*')
        for pr in prs:
            app.client.chat_postMessage(channel=channel_id, text=pr)
