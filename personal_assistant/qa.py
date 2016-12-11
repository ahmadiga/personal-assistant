try:
    from .common import *
except ImportError:
    pass

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'user',
        'PASSWORD': 'pass',
        'HOST': 'mysql',
        'PORT': '3306',
    },
}

STATIC_ROOT = "/usr/src/static/server"
ALLOWED_HOSTS = ["*", ]

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "asgi_ipc.IPCChannelLayer",
        "ROUTING": "main.routing.channel_routing",
        "CONFIG": {
            "prefix": "django",
        },
    },
}
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'memcache:11211',
    }
}
DEBUG = False
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/usr/src/debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
DEBUG = False

# ANYMAIL : mailgun configuration
ANYMAIL = {
    "MAILGUN_API_KEY": "< your api key at mailgun >",
    "MAILGUN_SENDER_DOMAIN": "< your sender domain at mailgun >"
}
EMAIL_BACKEND = "anymail.backends.mailgun.MailgunBackend"
DEFAULT_FROM_EMAIL = " <<your default from email>>"