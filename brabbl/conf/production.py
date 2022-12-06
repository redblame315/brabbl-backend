from .base_public import *


SITE_DOMAIN = 'api.brabbl.com'

ALLOWED_HOSTS = ['api.brabbl.com']

SESSION_COOKIE_SECURE = True

GUNICORN_PID_FILE = os.path.expanduser('~brabbl/run/gunicorn.pid')

SOCIAL_AUTH_FACEBOOK_KEY = '434164923308131'
SOCIAL_AUTH_FACEBOOK_SECRET = 'e546fe88649395b16e9b49e65995279c'

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = '324785695604-313q8nvu33j6rvk1vu9dqs7v2v6vb5ic.apps.googleusercontent.com'
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = 'Jk4OUEkJFrNCtqD5Hlb2ytjP'

SOCIAL_AUTH_TWITTER_KEY = '2xfH4hTXH6Q7UW9TmDDYMV45J'
SOCIAL_AUTH_TWITTER_SECRET = 'zqTcCoO6q8NBFWBqgPwS1Fe2O8nVRt1zvsdkG8CBW5LNu0Ad0u'

THEME_LOCATION_URL = 'https://api.brabbl.com/embed/themes/'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'sslout.df.eu'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'api@brabbl.com'
EMAIL_HOST_PASSWORD = 'fosqit-cakcUn-demjo0'
EMAIL_USE_SSL = True
