import os
from dotenv import load_dotenv
from slack import WebClient
from flask import Flask, request, make_response, Response
import json

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)

RECEIVER_ID = slack_client.auth_test()['user_id']

app = Flask(__name__)


@app.route("/webmonitor/actions", methods=["POST"])
def message_event_handler():
    req = json.loads(request.form["payload"])
    action = req.get('actions')[0].get('value')
    print(action)
    slack_client.chat_postMessage(channel='#web-monitor', text=f"{action} pressed!")

    return make_response("Great", 200)


def send():
    msg = {
        "channel": '#web-monitor',
        "text": "New Paid Time Off request from Fred Enriquez",
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New request",
                    "emoji": True
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Type:*\nPaid Time Off"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Created by:*\n<example.com|Fred Enriquez>"
                    }
                ]
            },
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"Hey there <@user>!"},
                "accessory": {
                    "type": "button",
                    "text": {"type": "plain_text", "text": "Click Me"},
                    "action_id": "button_click"
                }
            },
            {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*When:*\nAug 10 - Aug 13"
                    }
                ]
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Approve"
                        },
                        "style": "primary",
                        "value": "Approve_me_123"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "emoji": True,
                            "text": "Reject"
                        },
                        "style": "danger",
                        "value": "Reject_123"
                    }
                ]
            }
        ]
    }
    slack_client.chat_postMessage(**msg)

if __name__ == '__main__':
    send()
    app.run()