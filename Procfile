release: python manage.py migrate --no-input
release: django-admin compilemessages
web: gunicorn salon-ulm-blois.wsgi --log-file -
