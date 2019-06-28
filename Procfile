release: python manage.py migrate
release: django-admin compilemessages
web: gunicorn salon-ulm-blois.wsgi --log-file -
