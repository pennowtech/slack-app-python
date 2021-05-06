from slack import WebClient
import os
from dotenv import load_dotenv
from flask import Flask, request, make_response
import hmac
import hashlib

load_dotenv()
slack_client = WebClient(token=os.environ['SLACK_API_TOKEN'])

SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']

app = Flask(__name__)


# I got this code from online. However, missed the web url. 
# Credit goes to its author
def verify(request):
    data = request.get_data()

    timestamp = request.headers['X-Slack-Request-Timestamp']
    sig_basestring = f"v0:{timestamp}:{data.decode('utf-8')}"
    computed_sha = hmac.new(SLACK_SIGNING_SECRET.encode() ,
                            sig_basestring.encode('utf-8'),
                            digestmod=hashlib.sha256).hexdigest()
    my_sig = 'v0=%s' % (computed_sha,)
    slack_sig = request.headers['X-Slack-Signature']
    if my_sig != slack_sig:
        err_str = ("*Invalid request signature detected* "
                   f"\n*slack_sig:* {slack_sig}, \n*my_sig:* {my_sig})")
        return ({"status": 401, "error": err_str})
    
    return ({"status": 201, "error": 'Passed'})


@ app.route('/req-verify', methods=['POST'])
def curtime_command_handler():
    resp = verify(request)

    req_data = request.form
    channel_id = req_data.get('channel_id')
    slack_client.chat_postMessage(channel=channel_id, text=resp["error"])

    return make_response(resp['error'], resp['status'])


if __name__ == '__main__':
    app.run(debug=True)
