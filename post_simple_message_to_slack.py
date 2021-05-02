from slack import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

slack_client.chat_postMessage(channel='#web-monitor', text="Hello!")
# slack_client.chat_postMessage(channel='#general', text="Hello!")
