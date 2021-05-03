import os
from dotenv import load_dotenv
from slack import WebClient
from slackeventsapi import SlackEventAdapter


load_dotenv()

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SLACK_API_TOKEN = token=os.environ['SLACK_API_TOKEN']

slack_client = WebClient(SLACK_API_TOKEN)

RECEIVER_ID = slack_client.auth_test()['user_id']


slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET,
                                         "/webmonitor/events")

# Create an event listener for "message" events
@slack_events_adapter.on('message')
def message_event_handler(payload):
    event = payload.get('event')
    channel_id = event.get('channel')
    user_id = event.get('user')
    user_info = slack_client.users_info(user=user_id)
    user_name = user_info.get('user').get('name')
    
    if (RECEIVER_ID != user_id):
        response = f'Welcome <@{user_name}>! :wave:'
        slack_client.chat_postMessage(channel=channel_id, text=response)

# Example reaction emoji echo
# This will require us to subscribe to 'reaction_added' event from 'Event Subscriptions'
@slack_events_adapter.on("reaction_added")
def reaction_added(payload):
    event = payload["event"]
    emoji = event["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    slack_client.chat_postMessage(channel=channel, text=text)


if __name__ == '__main__':
    slack_events_adapter.start(port=5000)
