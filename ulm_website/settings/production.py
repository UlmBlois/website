from .base import *
import dj_database_url
import django_heroku



DEBUG = False

ALLOWED_HOSTS = ['salon-ulm-blois.herokuapp.com']

DATABASES['default'].update(dj_database_url.config(conn_max_age=500, ssl_require=True))

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


# Activate Django-Heroku.
django_heroku.settings(locals())
