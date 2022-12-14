# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = '3d_nh^-ngs_%d_^51x=oae8n%j)r1-v+#ah$t$w+240jm2g((f'

DEBUG = False

SITE_NAME = 'Brabbl'

VERSION = '2.5.4'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_crontab',

    'corsheaders',
    'django_rq',
    'easy_thumbnails',
    'rest_framework.authtoken',
    'social_django',
    'rosetta',
    'ckeditor',
    'embed_video',

    'brabbl.accounts',
    'brabbl.api',
    'brabbl.core',
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'brabbl.accounts.middleware.CustomerMiddleware',
    'brabbl.accounts.middleware.AdminLocaleURLMiddleware',
    'brabbl.accounts.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'brabbl.urls'

AUTH_USER_MODEL = 'accounts.User'

WSGI_APPLICATION = 'brabbl.wsgi.application'

LANGUAGE_CODE = 'en'
LANGUAGES = [
    ('en', _('English')),
    ('de', _('Deutsch')),
    ('es', _('Spanish')),
    ('fr', _('French')),
    ('it', _('Italian')),
    ('el', _("Greek")),
    ('uk', _('Ukrainian')),
    ('ru', _('Russian'))
]

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL = '/media/'

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'APP_DIRS': True,
    'DIRS': (os.path.join(BASE_DIR, 'templates'),),
    'OPTIONS': {
        'debug': True,
        'context_processors': (
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'social_django.context_processors.backends',
            'social_django.context_processors.login_redirect',
            'brabbl.core.context_processors.global_variables',
        ),
    },
}]

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

AUTHENTICATION_BACKENDS = (
    'social_core.backends.twitter.TwitterOAuth',
    'social_core.backends.google.GoogleOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',
    'django.contrib.auth.backends.ModelBackend',
)

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'brabbl.accounts.authentication.BrabblTokenAuthentication',
    ],
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    ),
    'DEFAULT_VERSIONING_CLASS': 'rest_framework.versioning.NamespaceVersioning',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'brabbl',
        'USER': 'postgres',
        'PASSWORD': 'kshpassword',
        'CONN_MAX_AGE': 300,
    },
}

DATA_UPLOAD_MAX_MEMORY_SIZE = 31457280
FILE_UPLOAD_MAX_MEMORY_SIZE = 31457280
FILE_UPLOAD_PERMISSIONS = 0o644

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'x-requested-with',
    'content-type',
    'accept',
    'origin',
    'authorization',
    'x-csrftoken',
    'x-brabbl-token'
)

LOGIN_URL = '/api/v1/account/login/'

# ---- brabbl-specific settings ------
SESSION_COOKIE_SECURE = False
DEFAULT_FROM_EMAIL = 'support@brabbl.com'
DEFAULT_USER_RATING = 3

# users need to confirm their email after this amount of days
MAX_EMAIL_CONFIRMATION_DAYS = 7

CRONJOBS = [
    ('0 16 * * *', 'django.core.management.newsmail'),
    ('0 14 * * *', 'django.core.management.non_confirmed_users_warning_letter'),
    # ('0 2 * * *', 'django.core.management.delete_non_confirmed_users'),
]

SOCIAL_AUTH_FIELDS_STORED_IN_SESSION = ['customer_token', 'back_url']
SOCIAL_AUTH_STORAGE = 'brabbl.accounts.social.Storage'
SOCIAL_AUTH_STRATEGY = 'brabbl.accounts.social.Strategy'
SOCIAL_AUTH_PROTECTED_USER_FIELDS = ['first_name', 'last_name']

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'brabbl.accounts.pipeline.social_user',
    'social_core.pipeline.user.get_username',
    'brabbl.accounts.pipeline.associate_by_email',
    'brabbl.accounts.pipeline.create_user',
    'brabbl.accounts.pipeline.associate_user',
    'brabbl.accounts.pipeline.load_extra_data',
    'social_core.pipeline.user.user_details',
    'brabbl.accounts.pipeline.finish_auth',
)

SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id,name,email',
}
SOCIAL_AUTH_GOOGLE_OAUTH2_IGNORE_DEFAULT_SCOPE = True
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = [
    'https://www.googleapis.com/auth/userinfo.email',
    'https://www.googleapis.com/auth/userinfo.profile'
]

EMBED_VIDEO_BACKENDS = (
    'embed_video.backends.YoutubeBackend',
)

WIDGET_HASHTAG = '#brabbl-widget'
