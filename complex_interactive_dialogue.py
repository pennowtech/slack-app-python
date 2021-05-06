import os
from dotenv import load_dotenv
from slack import WebClient

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)


def get_dialog_data_with_attachments():
    dialog_data = {
        "text": "Text to display in desktop/mobile notifications",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Danny Torrence left the following review for your property:"
                }
            },
            {
                "type": "section",
                "block_id": "section567",
                "text": {
                    "type": "mrkdwn",
                    "text": "<https://example.com|Overlook Hotel> \n :star: \n Doors had too many axe holes, guest in room 237 was far too rowdy, whole place felt stuck in the 1920s."
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://is5-ssl.mzstatic.com/image/thumb/Purple3/v4/d3/72/5c/d3725c8f-c642-5d69-1904-aa36e4297885/source/256x256bb.jpg",
                    "alt_text": "Haunted hotel image"
                }
            },
            {
                "type": "section",
                "block_id": "section789",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Average Rating*\n1.0"
                    }
                ]
            }
        ],
        "attachments": [
            {
                "color": "#2eb886",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": "*Alternative hotel options*"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                                    "text": "<https://example.com|Bates Motel> :star::star:"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View",
                                "emoji": True
                            },
                            "value": "view_alternate_1"
                        }
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                                    "text": "<https://example.com|The Great Northern Hotel> :star::star::star::star:"
                        },
                        "accessory": {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "View",
                                "emoji": True
                            },
                            "value": "view_alternate_2"
                        }
                    },
                    {
                        "type": "context",
                        "elements": [
                                {
                                    "type": "image",
                                    "image_url": "https://image.freepik.com/free-photo/red-drawing-pin_1156-445.jpg",
                                    "alt_text": "images"
                                },
                            {
                                    "type": "mrkdwn",
                                    "text": "Location: *Dogpatch*"
                                    },
                            {
                                    "type": "mrkdwn",
				                            "text": "<!date^1392734382^{date} at {time}|February 18th, 2014 at 6:39 AM PST> (PST)"
                                    }
                        ]
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
    msg = {**header, **get_dialog_data_with_attachments()}
    slack_client.chat_postMessage(**msg)


if __name__ == '__main__':
    send()
