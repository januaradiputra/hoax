release: python oke/manage.py makemigrations --no-input
release: python oke/manage.py migrate --no-input

web: gunicorn oke.wsgi --pythonpath=oke --log-file -
