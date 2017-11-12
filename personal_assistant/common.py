"""
Django settings for personal_assistant project.

Generated by 'django-admin startproject' using Django 1.9.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
from kombu import Exchange, Queue

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '=%2h+%ebz(7*y6)i8eoycf*ej)3-+tps1e8noajd_%9jvqlc^u'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 3rd party
INSTALLED_APPS += [
    "compressor",
    'djangobower',
    'crispy_forms',
    'channels',
    'sit_builder',
    'parsley',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.slack',
    'anymail',
    'django_celery_beat',
    'explorer',
    'report_builder',
    'bootstrap3_datepicker',
]

# Django debug toolbar settings

# my apps
INSTALLED_APPS += [
    'time_tracker',
    'attendance',
    "main",
    "absence",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'personal_assistant.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'absence.context_processors.count_pending'
            ],
        },
    },
]



WSGI_APPLICATION = 'personal_assistant.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Amman'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'djangobower.finders.BowerFinder',
    'compressor.finders.CompressorFinder',
)
BOWER_COMPONENTS_ROOT = BASE_DIR + '/'
BOWER_PATH = 'bower'
BOWER_INSTALLED_APPS = (
    'moment#2.17.1',
    'eonasdan-bootstrap-datetimepicker#latest'
)
COMPRESS_PRECOMPILERS = (
    ('text/scss', 'sass --scss --compass {infile} {outfile}'),
)
COMPRESS_URL = "/static/"

# Django registration
ACCOUNT_ACTIVATION_DAYS = 7

# Crispy forms
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Auth backends
AUTHENTICATION_BACKENDS = [
    'personal_assistant.auth_backends.EmailOrUsernameModelBackend',
]

# set login roles
# Choices
# email_username
# email
# username
DSK_LOGIN_FIELDS = "email_username"

SITE_ID = 1

SOCIALACCOUNT_PROVIDERS = {
    'slack': {
        'SCOPE': ['im:read', 'im:write', ]
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smt`p.EmailBackend'

SLACK_TOKEN = "<insert slack bot token>"
SLACK_ATTENDANCE_CHANNEL = "#insert-channel-here"
# CELERY STUFF
BROKER_URL = 'redis://redis:6379'
CELERY_RESULT_BACKEND = 'redis://redis:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Amman'
