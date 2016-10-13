"""
Django settings for hstool project.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

DEBUG = False
SECRET_KEY = '3-bj=-7$fh&)yf5m-d$dif07f86g=9x**9det1rzplg=dc64gq'

# Application definition

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'gunicorn',
    'django_assets',
    'widget_tweaks',
    'frame',
    'flis_metadata.common',
    'flis_metadata.client',
    'hstool',
    'raven.contrib.django.raven_compat',
)

MIDDLEWARE_CLASSES = (
    'frame.middleware.RequestMiddleware',
    'frame.middleware.UserMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'frame.middleware.SeenMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'frame.backends.FrameUserBackend',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.request',
            ],
            'loaders': [
                'frame.loaders.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ],
        }
    }
]

ROOT_URLCONF = 'hstool.urls'

WSGI_APPLICATION = 'hstool.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

DATE_FORMAT = 'j F Y'

DATE_INPUT_FORMATS = ('%d %B %Y',)

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = True

# Dynamic config
FORCE_SCRIPT_NAME = os.environ.get('FORCE_SCRIPT_NAME', '')
if FORCE_SCRIPT_NAME:
    USE_X_FORWARDED_HOST = True

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = FORCE_SCRIPT_NAME + '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'public', 'static')

MEDIA_URL = '/media/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FRAME_SEEN_MODELS = (
    ('hstool.models.Assessment', 'added'),
)

FRAME_SEEN_EXCLUDE = ('/_lastseencount/', )

# set this variable to the file types accepted when uploading facts and figures.
# any type is accepted if it is set to be the empty list [].
SUPPORTED_FILES_FACTS_AND_FIGURES = [
    'application/pdf', 'image/jpg', 'image/jpeg', 'image/png', 'image/gif',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
    'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    'application/msword',
    'application/vnd.ms-excel',
    'application/vnd.ms-powerpoint',
]

METADATA_URL = ''

if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass
else:
    try:
        from local_settings import *
    except ImportError:
        pass
