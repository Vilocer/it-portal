cd it_portal
gunicorn -c gunicorn_config.py config.wsgi
