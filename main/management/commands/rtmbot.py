import re
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import time

from django.urls import reverse
from nltk.chat.util import Chat, reflections
from slackclient import SlackClient

from attendance.models import Attendance
from main.management.commands.cleverwrap import CleverWrap
from main.models import Profile, MyUser
from django.db.models import Q, Sum, Avg
from cleverbot import Cleverbot
from django.utils import timezone

from main.templatetags.calculate_hours import calculate_hours
from main.utils.slack import post_message_on_channel, get_slack_user


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    outputs = []
    sc = None
    rude_chatbot = None
    pairs = None

    def __init__(self):
        slack_token = settings.SLACK_TOKEN
        self.sc = SlackClient(slack_token)
        self.pairs = (
            (r'We (.*)',
             ("What do you mean, 'we'?",
              "Don't include me in that!",
              "I wouldn't be so sure about that.")),

            (r'You should (.*)',
             ("Don't tell me what to do, buddy.",
              "Really? I should, should I?")),

            (r'You\'re(.*)',
             ("More like YOU'RE %1!",
              "Hah! Look who's talking.",
              "Come over here and tell me I'm %1.")),

            (r'You are(.*)',
             ("More like YOU'RE %1!",
              "Hah! Look who's talking.",
              "Come over here and tell me I'm %1.")),

            (r'I can\'t(.*)',
             ("You do sound like the type who can't %1.",
              "Hear that splashing sound? That's my heart bleeding for you.",
              "Tell somebody who might actually care.")),

            (r'I think (.*)',
             ("I wouldn't think too hard if I were you.",
              "You actually think? I'd never have guessed...")),

            (r'I (.*)',
             ("I'm getting a bit tired of hearing about you.",
              "How about we talk about me instead?",
              "Me, me, me... Frankly, I don't care.")),

            (r'How (.*)',
             ("How do you think?",
              "Take a wild guess.",
              "I'm not even going to dignify that with an answer.")),

            (r'What (.*)',
             ("Do I look like an encyclopedia?",
              "Figure it out yourself.")),

            (r'Why (.*)',
             ("Why not?",
              "That's so obvious I thought even you'd have already figured it out.")),

            (r'(.*)shut up(.*)',
             ("Make me.",
              "Getting angry at a feeble NLP assignment? Somebody's losing it.",
              "Say that again, I dare you.")),

            (r'Shut up(.*)',
             ("Make me.",
              "Getting angry at a feeble NLP assignment? Somebody's losing it.",
              "Say that again, I dare you.")),

            (r'Hello(.*)',
             ("Oh good, somebody else to talk to. Joy.",
              "'Hello'? How original...")),

            (r'(.*)',
             ("I'm getting bored here. Become more interesting.",
              "Either become more thrilling or get lost, buddy.",
              "Change the subject before I die of fatal boredom.")),

        )
        self.rude_chatbot = CleverWrap("CC3c5uETuZZM8N4GcclAUE_EIxw")

    def test(self, txt, txt2):
        print("Asdasdasdasd")
        print(txt)
        return "Checking if " + txt + " " + txt2

    def handle(self, *args, **options):

        if self.sc.rtm_connect():
            while True:
                for data in self.sc.rtm_read():
                    if "type" in data and data["type"] == "message":
                        self.handle_message(data)
                self.output()
                time.sleep(0.5)
        else:
            print("Connection Failed, invalid token?")

    def get_user_current_tasks(self, name, data):
        user_info = self.sc.api_call('users.info', user=name)
        profile = Profile.objects.get(slack_username=user_info["user"]["name"])
        if profile.user.attendance_set.filter(check_out__isnull=True):
            working_on = profile.user.timeentry_set.filter(ended_at__isnull=True).first()
            if working_on:
                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> Currently working on " + working_on.title
                     ]
                )
            else:
                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> is Free"
                     ]
                )

        else:
            self.outputs.append(
                [data['channel'],
                 "<@" + name + "> is not at the office now "
                 ]
            )
        pass

    def get_user_attendance(self, name, data):
        user_info = self.sc.api_call('users.info', user=name)
        profile = Profile.objects.get(slack_username=user_info["user"]["name"])
        if profile.user.attendance_set.filter(check_out__isnull=True):
            self.outputs.append(
                [data['channel'],
                 "<@" + name + "> is at the Office"
                 ]
            )

        else:
            self.outputs.append(
                [data['channel'],
                 "<@" + name + "> is not at the office now "
                 ]
            )

    def get_free_users(self, data):
        free_users = MyUser.objects.filter(
            Q(~Q(timeentry__ended_at__isnull=True) & Q(attendance__isnull=False) & Q(
                attendance__check_out__isnull=True))).distinct()
        str = ""
        for free_user in free_users:
            if hasattr(free_user, "profile") and free_user.profile.slack_username:
                str += "<@" + free_user.profile.slack_username + "> "
            else:
                str += free_user.username + " "

        if str:
            self.outputs.append(
                [data['channel'],
                 str + " can help you"
                 ]
            )

        else:
            self.outputs.append(
                [data['channel'],
                 "no one can help you now"
                 ]
            )

    def check_if_user_free(self, data):
        regexs = [
            '((\<@(?P<name>(?!U3GB3CH7X)\w+)\>).*(?P<action>free|available|has nothing to do))',
            '((?P<action>free|available|has nothing to do).*(\<@(?P<name>(?!U3GB3CH7X)\w+)\>))',
            '((?P<action>what are you doing).*(\<@(?P<name>(?!U3GB3CH7X)\w+)\>))',
            '((what).*(\<@(?P<name>(?!U3GB3CH7X)\w+)\>).*(?P<action>doing))',
            '((\<@(?P<name>(?!U3GB3CH7X)\w+)\>).*(?P<action>what are you doing))',
        ]
        for regex in regexs:
            m = re.search(regex, data['text'])
            if m:
                self.outputs.append(
                    [data['channel'],
                     "hmm, Let me see"
                     ]
                )
                try:
                    self.get_user_current_tasks(m.group("name"), data);
                except:
                    self.outputs.append(
                        [data['channel'],
                         "i don't know him sorry :S"
                         ]
                    )
                return True
        return False

    def check_if_at_office(self, data):
        regexs = [
            '((\<@(?P<name>(?!U3GB3CH7X)\w+)\>).*(?P<action>here|at the office))',
        ]
        for regex in regexs:
            m = re.search(regex, data['text'])
            if m:
                self.outputs.append(
                    [data['channel'],
                     "hmm, Let me see"
                     ]
                )
                try:
                    self.get_user_attendance(m.group("name"), data)
                except:
                    self.outputs.append(
                        [data['channel'],
                         "i don't know him sorry :S"
                         ]
                    )
                return True
        return False

    def check_if_who_is_free(self, data):
        regexs = [
            '(.*(?P<who>anyone|who).*(?P<action>here|free|available|help))',
        ]
        for regex in regexs:
            m = re.search(regex, data['text'])
            if m:
                self.outputs.append(
                    [data['channel'],
                     "hmm, Let me see"
                     ]
                )
                self.get_free_users(data)
                return True
        return False

    def checkout_user(self, name, data):
        user_info = self.sc.api_call('users.info', user=name)
        profile = Profile.objects.get(slack_username=user_info["user"]["name"])
        if profile:
            attendance = Attendance.objects.filter(check_out=None, user=profile.user).first()
            if attendance:
                attendance.check_user_out()
                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> Done"
                     ]
                )
                post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                        get_slack_user(profile.user) + " checked out from SIT office @ " + str(
                                            timezone.localtime(
                                                timezone.now()).strftime(
                                                "%Y-%m-%d %H:%M")) + "\n duration: " + calculate_hours(
                                            int(
                                                attendance.duration)) + "\n for more info please visit " + settings.SITE_URL + str(
                                            reverse("user_status", kwargs={"username": profile.user.username})))

            else:
                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> You are not checked in"
                     ]
                )
        else:
            self.outputs.append(
                [data['channel'],
                 "<@" + name + "> I dont know which whizz user you are update your profile to let me know"
                 ]
            )

    def check_if_checkout(self, data):
        regexs = [
            '(?P<action>check me out)',
        ]
        for regex in regexs:
            m = re.search(regex, data['text'])
            if m:
                self.outputs.append(
                    [data['channel'],
                     "give me a minute"
                     ]
                )
                try:
                    self.checkout_user(data['user'], data)
                except:
                    self.outputs.append(
                        [data['channel'],
                         "i don't know him sorry :S"
                         ]
                    )
                return True
        return False

    def checkin_user(self, name, data):
        user_info = self.sc.api_call('users.info', user=name)
        profile = Profile.objects.get(slack_username=user_info["user"]["name"])
        if profile:
            if not Attendance.objects.filter(check_out=None, user=profile.user):
                attendances = Attendance.objects.create(user=profile.user)

                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> Done"
                     ]
                )
                post_message_on_channel(settings.SLACK_ATTENDANCE_CHANNEL,
                                        get_slack_user(profile.user) + " checked in at SIT office @ " + str(
                                            timezone.localtime(timezone.now()).strftime(
                                                "%Y-%m-%d %H:%M")) + "\n for more info please visit" + settings.SITE_URL + str(
                                            reverse("user_status", kwargs={"username": profile.user.username})))
            else:
                self.outputs.append(
                    [data['channel'],
                     "<@" + name + "> You are already checked in"
                     ]
                )
        else:
            self.outputs.append(
                [data['channel'],
                 "<@" + name + "> I dont know which whizz user you are update your profile to let me know"
                 ]
            )

    def check_if_checkin(self, data):
        regexs = [
            '(?P<action>check me in)',
        ]
        for regex in regexs:
            m = re.search(regex, data['text'])
            if m:
                self.outputs.append(
                    [data['channel'],
                     "give me a minute"
                     ]
                )
                print(data)
                try:
                    self.checkin_user(data['user'], data)
                except:
                    self.outputs.append(
                        [data['channel'],
                         "i don't know him sorry :S"
                         ]
                    )
                return True
        return False

    def handle_message(self, data):
        if "text" in data:
            print(data)
            if self.check_if_user_free(data):
                return
            if self.check_if_at_office(data):
                return
            if self.check_if_who_is_free(data):
                return
            if (data['channel'].startswith("D") or "<@U3GB3CH7X>" in data["text"]) and self.check_if_checkout(data):
                return
            if (data['channel'].startswith("D") or "<@U3GB3CH7X>" in data["text"]) and self.check_if_checkin(data):
                return

            if data['channel'].startswith("D") or "<@U3GB3CH7X>" in data["text"] or "<!channel>" in data["text"]:
                msg = re.sub(r'(?P<me><@U3GB3CH7X>\s*|<!channel>\s*)', '', data["text"])
                self.outputs.append(
                    [data['channel'],
                     self.rude_chatbot.say(msg)
                     ]
                )

    def output(self):
        limiter = False
        for output in self.outputs:
            channel = self.sc.server.channels.find(output[0])
            if channel is not None and output[1] is not None:
                if limiter:
                    time.sleep(.1)
                    limiter = False
                channel.send_message(output[1])
                limiter = True
        self.outputs = []
