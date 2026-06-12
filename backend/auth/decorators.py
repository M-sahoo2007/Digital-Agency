from functools import wraps
from flask import request, jsonify, g
from models import User, db
from auth.jwt_handler import decode_access_token
import jwt


def token_required(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
      return jsonify({'error': 'Authorization token required'}), 401

    token = auth_header.split(' ', 1)[1]
    try:
      payload = decode_access_token(token)
      user = db.session.get(User, payload['sub'])
      if not user:
        return jsonify({'error': 'User not found'}), 401
      g.current_user = user
    except jwt.ExpiredSignatureError:
      return jsonify({'error': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
      return jsonify({'error': 'Invalid token'}), 401

    return f(*args, **kwargs)
  return decorated


def admin_required(f):
  @wraps(f)
  @token_required
  def decorated(*args, **kwargs):
    if not g.current_user.is_admin():
      return jsonify({'error': 'Admin access required'}), 403
    return f(*args, **kwargs)
  return decorated
