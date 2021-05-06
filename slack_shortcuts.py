import os
from dotenv import load_dotenv
from slack_sdk import WebClient
from flask import Flask, request, make_response, Response
import json
import dpath.util

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(token=SLACK_API_TOKEN)

app = Flask(__name__)


def get_dialog_data():
    dialog_data = {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Web Monitoring Configuration"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sl_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter URL"
                    }
                },
                "label": {
                    "type": "plain_text",
                            "text": "URL"
                },
                "hint": {
                    "type": "plain_text",
                            "text": "URL of website to be monitored"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select",
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Every Minute"
                            },
                            "value": "minuetly"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hourly"
                            },
                            "value": "hourly"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Daily"
                            },
                            "value": "daily"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                            "text": "Monitoring Frequency",
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Submit"
                        },
                        "style": "primary",
                        "value": "submit"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel"
                        },
                        "style": "danger",
                        "value": "cancel"
                    }
                ]
            }
        ]
    }

    return dialog_data


def data():
    d = {
        "type": "modal",
        "title": {
                "type": "plain_text",
                "text": "My App",
        },
        "submit": {
            "type": "plain_text",
            "text": "Submit",
        },
        "close": {
            "type": "plain_text",
            "text": "Cancel",
        },
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "Web Monitoring Configuration"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "sl_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter URL"
                    }
                },
                "label": {
                    "type": "plain_text",
                            "text": "URL"
                },
                "hint": {
                    "type": "plain_text",
                            "text": "URL of website to be monitored"
                }
            },
            {
                "type": "input",
                "element": {
                    "type": "static_select",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Every Minute"
                            },
                            "value": "minuetly"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Hourly"
                            },
                            "value": "hourly"
                        },
                        {
                            "text": {
                                "type": "plain_text",
                                "text": "Daily"
                            },
                            "value": "daily"
                        }
                    ],
                    "action_id": "static_select-action"
                },
                "label": {
                    "type": "plain_text",
                            "text": "Monitoring Frequency"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Submit"
                        },
                        "style": "primary",
                        "value": "submit"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Cancel"
                        },
                        "style": "danger",
                        "value": "cancel"
                    }
                ]
            }
        ]
    }

    return d


def send(channel_id):
    header = {
        "channel": channel_id,
    }
    msg = {**header, **data()}
    slack_client.chat_postMessage(**msg)


def extract_input_val(req):
    url_val = None
    frequency_val = None

    # URL input, and frequency selection entries are 4 level deep inside dictionary.
    url_val_dict = dpath.util.get(req, 'state/values/*/sl_input')
    frequency_dict = dpath.util.get(req, 'state/values/*/static_select-action')
    if url_val_dict:
        url_val = url_val_dict.get('value')
    if frequency_dict:
        frequency_dict = frequency_dict.get('selected_option', {}) or {}
        frequency_val = frequency_dict.get('value')

    return url_val, frequency_val


def verify_input(url_val, frequency_val):
    if url_val is None or frequency_val is None:
        return False
    else:
        return True


@app.route("/webmonitor/interactivity", methods=["POST"])
def message_event_handler():
    req = json.loads(request.form["payload"])
    channel_id = req.get('channel').get('id')

    # Check if shortcuts by verifying 'callback_id'
    if (req.get('callback_id') == 'website-monitor-cb'):
        send(channel_id)
        return make_response("", 200)

    action = req.get('actions')[0].get('value')
    if action is None:
        return make_response("", 200)

    if action == 'submit':
        url_val, frequency_val = extract_input_val(req)
        if verify_input(url_val, frequency_val):
            text = f'Monitoring service started for *{url_val}* at *{frequency_val}* interval!'
            slack_client.chat_postMessage(channel=channel_id, text=text)
        else:
            slack_client.chat_postMessage(
                channel=channel_id, text=':mega: *Enter inputs for URL and Frequency*')
    elif action == 'cancel':
        msg = ':warning: Cancel button is pressed. Nothing to do.'
        slack_client.chat_postMessage(channel=channel_id, text=msg)

    return make_response("Geat", 200)


if __name__ == '__main__':
    app.run(debug=True)
