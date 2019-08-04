from .base import *
import os
import logging.config
from django.utils.log import DEFAULT_LOGGING

from dotenv import load_dotenv
from pathlib import Path  # python3 only


# OR, explicitly providing path to '.env'

env_path = Path('/home/genos/website/website/salon_ulm_blois/settings/.env')
load_dotenv(dotenv_path=env_path)


DEBUG = False

SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

SECURE_BROWSER_XSS_FILTER = True

SECURE_CONTENT_TYPE_NOSNIFF = True

SECURE_HSTS_SECONDS = 31536000

SECRET_KEY = os.environ.get('ULM_SECRET_KEY', 'amf$+%4%7-vr-dfrq#x$(#ge_491e=4uoered%ujytoq@o3og0')

ALLOWED_HOSTS = ['ulm-blois.fr', 'www.ulm-blois.fr']

DEFAULT_DOMAIN = 'ulm-blois.fr'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('ULM_DB_NAME', ''),
        'USER': os.environ.get('ULM_DB_USER', ''),
        'PASSWORD': os.environ.get('ULM_DB_PASSWORD', ''),
        'HOST': 'localhost',
        'PORT': '',
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('ULM_EMAIL_HOST', '')
EMAIL_PORT = os.environ.get('ULM_EMAIL_PORT', 0)
EMAIL_HOST_USER = os.environ.get('ULM_EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('ULM_EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = 'no-reply@ulm-blois.fr'
EMAIL_USE_TLS = True

ADMINS = [('admin', 'admin@ulm-blois.fr')]
MANAGERS = [('manager', 'manager@ulm-blois.fr')]


X_FRAME_OPTIONS = 'DENY'
# Disable Django's logging setup
LOGGING_CONFIG = None

LOGLEVEL = os.environ.get('LOGLEVEL', 'DEBUG').upper()

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
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'default',
            'filename': os.environ.get('ULM_LOG_PATH', "/var/log/ulm-blois.fr/website.log"),
        },
        'mail_admins': {
            'level': 'ERROR',
            'formatter': 'default',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        },
        # Add Handler for Sentry for `warning` and above
        # 'sentry': {
        #     'level': 'WARNING',
        #     'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        # },
        'django.server': DEFAULT_LOGGING['handlers']['django.server'],
    },
    'loggers': {
        'django': {
            'level': LOGLEVEL,
            'handlers': ['file', 'mail_admins'],
            'propagate': True,
        },
        # default for all undefined Python modules
        '': {
            'level': LOGLEVEL,
            'handlers': ['file'],  # 'sentry'],
        },
        # Our application code
        'meeting': {
            'level': LOGLEVEL,
            'handlers': ['file'],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'core': {
            'level': LOGLEVEL,
            'handlers': ['file'],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'pages': {
            'level': LOGLEVEL,
            'handlers': ['file'],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'command': {
            'level': LOGLEVEL,
            'handlers': ['console', 'file'],  # 'sentry'],
            # Avoid double logging because of root logger
            # 'propagate': False,
        },
        # Prevent noisy modules from logging to Sentry
        'noisy_module': {
            'level': 'ERROR',
            'handlers': ['file'],
            'propagate': False,
        },
        # Default runserver request logging
        'django.server': DEFAULT_LOGGING['loggers']['django.server'],
    },
})
