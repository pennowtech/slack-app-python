import os
from dotenv import load_dotenv
from slack import WebClient
from flask import Flask, request, make_response, Response
import json
import pytz
from datetime import datetime

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)

RECEIVER_ID = slack_client.auth_test()['user_id']

app = Flask(__name__)


def get_time(text):
    tz = None
    if text == 'local':
        tz = pytz.timezone('Europe/Berlin')
    elif text == 'remote':
        tz = pytz.timezone('Europe/London')

    response_txt = ''
    if tz is not None:
        cur_time = datetime.now(tz).strftime('%H:%M:%S')
        response_txt = f"Current time is: {cur_time}"
    else:
        response_txt = f"Invalid command."

    str = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"You asked for *{text}* time:"
                }
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': response_txt
                }
            }
        ]
    }

    return str


@ app.route('/curtime', methods=['POST'])
def curtime_command_handler():
    req_data = request.form
    channel_id = req_data.get('channel_id')

    text = req_data.get('text')

    header_txt = {
        "channel": channel_id,
    }
    response_txt = {**header_txt, **get_time(text)}
    slack_client.chat_postMessage(**response_txt)

    return Response(), 200


if __name__ == '__main__':
    app.run()
