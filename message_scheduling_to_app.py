import os
from dotenv import load_dotenv
from slack import WebClient
import datetime

load_dotenv()

SLACK_API_TOKEN = token = os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)

RECEIVER_ID = slack_client.auth_test()['user_id']

def send():
    # Create a timestamp for tomorrow at 9AM
    # datetime.datetime(2021, 5, 2, 9, 0).timestamp()

    # scheduled a message after 20 secs
    scheduled_time = datetime.datetime.now() + datetime.timedelta(seconds=20)

    slack_client.chat_scheduleMessage(
        channel='#web-monitor',
        post_at=scheduled_time.timestamp(),
        text="scheduleMessage: Summer has come and passed"
    )


if __name__ == '__main__':
    send()
