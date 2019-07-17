from .base import *
import logging.config
from django.utils.log import DEFAULT_LOGGING
import os

DEBUG = True
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'amf$+%4%7-vr-dfrq#x$(#ge_491e=4uoered%ujytoq@o3og0')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'travisci',
        'USER': 'postgres',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',
    }
}


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
        'core': {
            'level': LOGLEVEL,
            'handlers': ['console', ],  # 'sentry'],
            # Avoid double logging because of root logger
            'propagate': False,
        },
        'pages': {
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
