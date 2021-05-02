from slack import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

print(slack_client.api_test())

# Fetch channels through conversation_list API
conversations_list = slack_client.conversations_list(
    types="public_channel, private_channel"
)

# PRint channels
if conversations_list.get('ok'):
    channels_list = conversations_list['channels']
    for channel in channels_list:
        print(channel['name'] + " (" + channel['id'] + ")")
