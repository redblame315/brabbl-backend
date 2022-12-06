import os.path

from .base import *


MEDIA_ROOT = os.path.expanduser('~brabbl/media')
STATIC_ROOT = os.path.expanduser('~brabbl/static')

RAVEN_CONFIG = {
    'dsn': 'https://956640c85d4742d5909571937fc54496:' +
           '17cb495513bc40d2895502506a4d4067@sentry.io/96921'
}

INSTALLED_APPS.append('raven.contrib.django.raven_compat')

RQ_QUEUES = {
    'default': {
        'HOST': 'localhost',
        'PORT': 6379,
        'DB': 1,
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d '
                      '%(thread)d %(message)s'
        },
        'simple': {
            'format': '>>> %(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'sentry': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.handlers.SentryHandler',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.db': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'requests': {
            'level': 'WARNING',
        },
        'py.warnings': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'WARNING',
            'handlers': ['console'],
            'propagate': False,
        },
        '': {
            'handlers': ['console', 'sentry'],
            'level': 'DEBUG',
        },
    },
}
