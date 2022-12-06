from .base_public import *

MEDIA_ROOT = os.path.expanduser('~brabbl-new_staging/media')
STATIC_ROOT = os.path.expanduser('~brabbl-new_staging/static')

SESSION_COOKIE_SECURE = True
ALLOWED_HOSTS = ['staging.brabbl.com', 'www.staging.brabbl.com']
SITE_DOMAIN = 'staging.brabbl.com'
DATABASES['default']['NAME'] = 'brabbl-new_staging'
GUNICORN_PID_FILE = os.path.expanduser('~brabbl-new_staging/run/gunicorn.pid')

SOCIAL_AUTH_FACEBOOK_KEY = '902185183942953'
SOCIAL_AUTH_FACEBOOK_SECRET = '464585baca6e89dca9eabf898c197712'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '1029460231592-pisjnovaqrodmbbeg7g6r9fcj8m9pfh7.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'sk3AN9Z1JGLamrVT75wkVJkP'

SOCIAL_AUTH_TWITTER_KEY = 'krescoig24pXrl770SEQHg3jC'
SOCIAL_AUTH_TWITTER_SECRET = 'chtCALsHS1OSSIKmWq7FlTMzQNKiD1GVl7fvWgkOynjnMjkDrQ'

THEME_LOCATION_URL = 'https://staging.brabbl.com/embed/themes/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sslout.df.eu'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'api@brabbl.com'
EMAIL_HOST_PASSWORD = 'fosqit-cakcUn-demjo0'
EMAIL_USE_SSL = True
