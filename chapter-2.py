from slack import WebClient
import os
from dotenv import load_dotenv

load_dotenv()
slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

slack_client.chat_postMessage(channel='#web-monitor', text="Hello!")

# def send_message(channel_id, message):
#     slack_client.chat_postMessage({
#         'channel':channel_id,
#         'text':message,
#         'username':'pythonbot',
#         'icon_emoji':':robot_face:'
#     })

def send_message(channel_id, message):
    slack_client.chat_postMessage(channel='#web-monitor', text="Hello")

def list_channels():

    channels_call = slack_client.conversations_list(
        types="public_channel, private_channel"
    )
    if channels_call.get('ok'):
        return channels_call['channels']
    return None


if __name__ == '__main__':
    channels = list_channels()
    if channels:
        print("Channels: ")
        for channel in channels:
            print(channel['name'] + " (" + channel['id'] + ")")
            if channel['name'] == 'general':
                send_message(channel['id'], "Hello " +
                             channel['name'] + "! It worked!")
        print('-----')
    else:
        print("Unable to authenticate.")