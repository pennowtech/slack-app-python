from slack import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

response = slack_client.chat_postMessage(channel='#web-monitor', text="Hello!")
timestamp = response['ts']

channel_id = response['channel']
slack_client.pins_add(timestamp=timestamp, channel= channel_id)