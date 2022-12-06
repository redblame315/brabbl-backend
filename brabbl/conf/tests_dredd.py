from .tests import *


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/tmp/brabbl_test.sqlite',
    }
}
