try:
    from personal_assistant.common import *
except ImportError:
    pass

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
STATIC_ROOT = os.path.join(BASE_DIR, '../statics')

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_ipc.IPCChannelLayer",
        "ROUTING": "main.routing.channel_routing",
        "CONFIG": {
            "prefix": "django",
        },
    },
}
# ANYMAIL : mailgun configuration
ANYMAIL = {
    "MAILGUN_API_KEY": "< your api key at mailgun >",
    "MAILGUN_SENDER_DOMAIN": "< your sender domain at mailgun >"
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
DEFAULT_FROM_EMAIL = " <<your default from email>>"

SITE_URL = "http://192.168.99.100:8000"
DEBUG_TOOLBAR_ENABLED = True

if DEBUG_TOOLBAR_ENABLED:
    INSTALLED_APPS += [
        'debug_toolbar',
    ]
    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


    def show_toolbar(request):
        return DEBUG_TOOLBAR_ENABLED


    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_TOOLBAR_CALLBACK": show_toolbar,
        "SHOW_COLLAPSED": True,
    }
