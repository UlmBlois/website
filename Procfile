release: python manage.py migrate --no-input
release: django-admin compilemessages
web: gunicorn salon_ulm_blois.wsgi --log-file -
