from app import create_app

# Exposto para servidores WSGI (Gunicorn, uWSGI)
app = create_app()
