import logging
import warnings
from .dev import *

COMPRESS_ROOT = ''
COMPRESS_ENABLED = False

TESTING = True

ALLOWED_HOSTS = ['*']

REST_FRAMEWORK['DEFAULT_AUTHENTICATION_CLASSES'].append(
    'rest_framework.authentication.SessionAuthentication')

# Disable all log messages that are less severe than critical
logging.disable(logging.WARNING)

# Stop whenever a naive datetime is being saved
warnings.filterwarnings(
    'error', r"DateTimeField .* received a naive datetime",
    RuntimeWarning, r'django\.db\.models\.fields')
