import os
from django.utils.translation import gettext_lazy as _
import logging.config
from django.utils.log import DEFAULT_LOGGING
from django.contrib.messages import constants as messages


BASE_DIR = os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'amf$+%4%7-vr-dfrq#x$(#ge_491e=4uoered%ujytoq@o3og0')

# Application definition

INSTALLED_APPS = [
    # Third parties apps
    'django_countries',
    'widget_tweaks',
    'django_filters',
    'betterforms',
    'translated_fields',
    'tinymce',
    'whitenoise.runserver_nostatic',
    'phonenumber_field',
    'crispy_forms',
    'extra_views',

    # Core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Project Apps
    'core.apps.CoreConfig',
    'meeting.apps.MeetingConfig',
    'pages.apps.PagesConfig',
    'faq.apps.FaqConfig',
    'radio_call_sign_field.apps.RadioCallSignFieldConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
]

ROOT_URLCONF = 'salon-ulm-blois.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'templates/base'),
            os.path.join(BASE_DIR, 'templates/errors'),
            os.path.join(BASE_DIR, 'templates/includes'),
            os.path.join(BASE_DIR, 'templates/emails'),
            os.path.join(BASE_DIR, 'templates/registration'),
            os.path.join(BASE_DIR, 'meeting/templates/includes/ajax'),
            os.path.join(BASE_DIR, 'meeting/templates/widgets'),
            os.path.join(BASE_DIR, 'pages/templates'),
            os.path.join(BASE_DIR, 'faq/templates'),
            ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'salon-ulm-blois.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

LOGIN_REDIRECT_URL = '/meeting/pilot/'
LOGOUT_REDIRECT_URL = '/'

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en'

LANGUAGES = [
    ('en', _('English')),
    ('fr', _('French')),
]

TIME_ZONE = 'Europe/Paris'

USE_TZ = True

USE_I18N = True

USE_L10N = True

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    os.path.join(BASE_DIR, 'meeting/static'),
)


MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


TINYMCE_DEFAULT_CONFIG = {
    'height': 360,
    'width': 1120,
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 20,
    'selector': 'textarea',
    'theme': 'modern',
    'plugins': '''
            textcolor save link image media preview codesample contextmenu
            table code lists fullscreen  insertdatetime  nonbreaking
            contextmenu directionality searchreplace wordcount visualblocks
            visualchars code fullscreen autolink lists  charmap print  hr
            anchor pagebreak
            ''',
    'toolbar1': '''
            fullscreen preview bold italic underline | fontselect,
            fontsizeselect  | forecolor backcolor | alignleft alignright |
            aligncenter alignjustify | indent outdent | bullist numlist table |
            | link image media | codesample |
            ''',
    'toolbar2': '''
            visualblocks visualchars |
            charmap hr pagebreak nonbreaking anchor |  code |
            ''',
    'contextmenu': 'formats | link image',
    'menubar': True,
    'statusbar': True,
    }


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

PHONENUMBER_DB_FORMAT = 'E164'
PHONENUMBER_DEFAULT_REGION = 'FR'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'info').upper()

logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            # exact format is not important, this is the minimum information
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
    },
    'handlers': {
        # console logs to stderr
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
        # Add Handler for Sentry for `warning` and above
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        # default for all undefined Python modules
        '': {
            'level': 'WARNING',
            'handlers': ['console', ],  # 'sentry'],
        },
        # Our application code
        'meeting': {
            'level': LOGLEVEL,
            'handlers': ['console', ],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'radio_call_sign_field': {
            'level': LOGLEVEL,
            'handlers': ['console', ],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        'noisy_module': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})


MESSAGE_TAGS = {
    messages.DEBUG: 'alert-info',
    messages.INFO: 'alert-info',
    messages.SUCCESS: 'alert-success',
    messages.WARNING: 'alert-warning',
    messages.ERROR: 'alert-danger',
}
