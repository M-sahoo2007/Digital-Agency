import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SQLITE_PATH = os.path.join(BASE_DIR, 'database', 'm_sahoo2007.db')


def resolve_database_uri():
  explicit = os.environ.get('DATABASE_URL', '').strip()
  if explicit:
    return explicit

  use_sqlite = os.environ.get('USE_SQLITE', 'true').lower() == 'true'
  if use_sqlite:
    os.makedirs(os.path.dirname(SQLITE_PATH), exist_ok=True)
    return f'sqlite:///{SQLITE_PATH.replace(os.sep, "/")}'

  return 'postgresql://postgres:postgres@localhost:5432/m_sahoo2007'


_DATABASE_URI = resolve_database_uri()


class Config:
  SECRET_KEY = os.environ.get('SECRET_KEY', 'msahoo2007-dev-secret-change-in-production')
  SQLALCHEMY_DATABASE_URI = _DATABASE_URI
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  SQLALCHEMY_ENGINE_OPTIONS = (
    {}
    if _DATABASE_URI.startswith('sqlite')
    else {'pool_pre_ping': True}
  )

  JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'msahoo2007-jwt-secret-change-in-production')
  JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=int(os.environ.get('JWT_EXPIRE_HOURS', 24)))

  MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
  MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
  MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
  MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
  MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
  MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@m-sahoo2007.com')
  ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@m-sahoo2007.com')

  CORS_ORIGINS = os.environ.get(
    'CORS_ORIGINS',
    'http://localhost:5500,http://127.0.0.1:5500,http://localhost:5000,http://127.0.0.1:5000'
  ).split(',')

  RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200 per hour')
  RATELIMIT_STORAGE_URI = os.environ.get('RATELIMIT_STORAGE_URI', 'memory://')
