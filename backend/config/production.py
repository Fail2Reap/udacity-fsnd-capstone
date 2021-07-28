import os

# Flask
TESTING = True if os.environ.get('FLASK_TESTING', None) else False
DEBUG = True if os.environ.get('FLASK_DEBUG', None) else False
ENV = os.environ.get('FLASK_ENV', 'production')
SECRET_KEY = os.environ['FLASK_SECRET_KEY']

# SQLAlchemy
SQLALCHEMY_DATABASE_URI = os.environ['FLASK_DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Auth
AUTH_DOMAIN = os.environ['AUTH_DOMAIN']
AUTH_ALGORITHM = os.environ['AUTH_ALGORITHM']
AUTH_API_AUDIENCE = os.environ['AUTH_API_AUDIENCE']
