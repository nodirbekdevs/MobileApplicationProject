from dotenv import load_dotenv
from os import environ

load_dotenv()

ENVIRON_SECRET_KEY = environ['SECRET_KEY']
ENVIRON_ALLOWED_HOSTS = [environ['ALLOWED_HOSTS']]
ENVIRON_DEBUG = environ['DEBUG']
ENVIRON_POSTGRES_USER = environ['POSTGRES_USER']
ENVIRON_POSTGRES_PASSWORD = environ['POSTGRES_PASSWORD']
ENVIRON_POSTGRES_HOST = environ['POSTGRES_HOST']
ENVIRON_POSTGRES_PORT = environ['POSTGRES_PORT']
ENVIRON_POSTGRES_DB = environ['POSTGRES_DB']
ENVIRON_DJANGO_SUPERUSER_USERNAME = environ['DJANGO_SUPERUSER_USERNAME']
ENVIRON_DJANGO_SUPERUSER_EMAIL = environ['DJANGO_SUPERUSER_EMAIL']
ENVIRON_DJANGO_SUPERUSER_PASSWORD = environ['DJANGO_SUPERUSER_PASSWORD']
