import os
from channels.asgi import get_channel_layer

import pymysql

pymysql.install_as_MySQLdb()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personal_assistant.settings")

channel_layer = get_channel_layer()
