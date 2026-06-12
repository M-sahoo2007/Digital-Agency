import jwt
from datetime import datetime, timezone
from flask import current_app


def create_access_token(user_id, role):
  payload = {
    'sub': user_id,
    'role': role,
    'iat': datetime.now(timezone.utc),
    'exp': datetime.now(timezone.utc) + current_app.config['JWT_ACCESS_TOKEN_EXPIRES'],
  }
  return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm='HS256')


def decode_access_token(token):
  return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
