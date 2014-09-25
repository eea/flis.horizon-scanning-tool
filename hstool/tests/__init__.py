import os

from django.conf import settings
from django_webtest import WebTest

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

MEDIA_ROOT_TEST = os.path.join(BASE_DIR, 'media_test')


class HSWebTest(WebTest):
    def _setup_auth_middleware(self):
        super(HSWebTest, self)._setup_auth_middleware()
        django_remote_middleware = \
            'django.contrib.auth.middleware.RemoteUserMiddleware'

        if django_remote_middleware in settings.MIDDLEWARE_CLASSES:
            settings.MIDDLEWARE_CLASSES.remove(django_remote_middleware)