release: cd oke
release: python manage.py makemigrations --no-input
release: python manage.py migrate --no-input

web: gunicorn oke.wsgi --pythonpath=oke --log-file -
