from .base import *

DEBUG = True

SITE_DOMAIN = 'localhost:8000'
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

STATICFILES_DIRS += (
    os.path.join(BASE_DIR, '..', 'frontend', 'dist'),
)

RQ_QUEUES = {
    'default': {
        'ASYNC': False,
    },
}

try:
    import django_extensions  # NOQA
except ImportError:
    pass
else:
    INSTALLED_APPS += ('django_extensions',)

SOCIAL_AUTH_FACEBOOK_KEY = '924534627675317'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e6b15a4ac7fe7b841401844d05c6be47'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    '108045976272-f3je9hkletrf7r6ucsmt7n5odnim9kov.apps.googleusercontent.com'
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'K3B7LMmDsPmS5q7Qvn4Qya9r'

SOCIAL_AUTH_TWITTER_KEY = '01RhbkG6Y5ZlgFdclV2QryEhF'
SOCIAL_AUTH_TWITTER_SECRET = 'xl2xpD3EvN3cpbe3ez9oR8fbR4bWD9m2JYU8RbpRT5KaweIehv'


TIME_ZONE = 'Europe/Berlin'

THEME_LOCATION_URL = 'http://localhost:8080/dist/build/staging/themes/'

STATIC_ROOT = 'static_files'
