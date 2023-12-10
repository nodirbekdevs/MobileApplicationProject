from dotenv import load_dotenv
from os import environ
from os.path import join, dirname, abspath

load_dotenv()

ORIGINS = eval(environ['ORIGINS'])
API_PREFIX = '/api'
ROUTE_PREFIX = '/v1'
HOST = environ['HOST']
ALGORITHM = environ['ALGORITHM']
SECRET_KEY = environ['SECRET_KEY']
TOKEN_EXPIRE_HOURS = environ['TOKEN_EXPIRE_HOURS']
AUTH_USERNAME = environ['AUTH_USERNAME']
AUTH_PASSWORD = environ['AUTH_PASSWORD']
DB_DIALECT = f"postgres://{environ['POSTGRES_USER']}:{environ['POSTGRES_PASSWORD']}@{environ['POSTGRES_HOST']}:{environ['POSTGRES_PORT']}/{environ['POSTGRES_DB']}"
BOT_TOKEN = environ['BOT_TOKEN']
ADMIN, SUPER_ADMIN, INSTRUCTOR, STUDENT = 'ADMIN', 'SUPER_ADMIN', 'INSTRUCTOR', 'STUDENT'
ADVERTISING, TEST, REPORT = 'ADVERTISING', 'TEST', 'REPORT'

uploads_file_path = join(dirname(abspath(__file__)), '..', '..', '..', 'uploads')
