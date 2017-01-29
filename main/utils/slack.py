from django.conf import settings
from slackclient import SlackClient


def get_slack_user(user):
    if hasattr(user, "profile") and user.profile.slack_username:
        return "<@" + user.profile.slack_username + ">"
    else:
        return str(user)


def post_message_on_channel(channel, text):
    slack_token = settings.SLACK_TOKEN
    sc = SlackClient(slack_token)
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=text,
        username="whizz",
        as_user=True
    )
