import os
from dotenv import load_dotenv
from slack import WebClient

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)



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


def send():
    header = {
        "channel": '#web-monitor',
    }
    msg = {**header, **get_dialog_data()}
    slack_client.chat_postMessage(**msg)


if __name__ == '__main__':
    send()


