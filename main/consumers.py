# In consumers.py
from channels import Channel, Group
import json
from channels.auth import http_session_user, channel_session_user, channel_session_user_from_http


@channel_session_user_from_http
def ws_add(message):
    # Add them to the right group
    Group("chat").add(message.reply_channel)


# Connected to websocket.receive
@channel_session_user
def ws_message(message):
    Group("chat").send({
        "text": json.dumps({
            "text": message['text'],
            "user": message.user.username,
        })
    })


# Connected to websocket.disconnect
@channel_session_user
def ws_disconnect(message):
    Group("chat").send({
        "text": json.dumps({
            "text": "has left the room",
            "user": message.user.username,
        })
    })
    Group("chat").discard(message.reply_channel)
