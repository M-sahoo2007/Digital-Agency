from flask import Blueprint, request, jsonify
from models import db, User
from auth.jwt_handler import create_access_token
from services.validation import validate_required_fields, validate_email_address, sanitize_string

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')


@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['name', 'email', 'password'])
  if not valid:
    return jsonify({'error': error}), 400

  name = sanitize_string(data['name'], 120)
  email = sanitize_string(data['email'], 255).lower()
  password = data['password']

  if len(password) < 8:
    return jsonify({'error': 'Password must be at least 8 characters'}), 400

  valid_email, email_error = validate_email_address(email)
  if not valid_email:
    return jsonify({'error': email_error}), 400

  if User.query.filter_by(email=email).first():
    return jsonify({'error': 'Email already registered'}), 409

  role = 'admin' if User.query.count() == 0 else 'user'
  if data.get('role') == 'admin' and User.query.filter_by(role='admin').count() > 0:
    role = 'user'

  user = User(name=name, email=email, role=role)
  user.set_password(password)
  db.session.add(user)
  db.session.commit()

  token = create_access_token(user.id, user.role)
  return jsonify({
    'message': 'Registration successful',
    'token': token,
    'user': user.to_dict(),
  }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['email', 'password'])
  if not valid:
    return jsonify({'error': error}), 400

  email = sanitize_string(data['email'], 255).lower()
  user = User.query.filter_by(email=email).first()

  if not user or not user.check_password(data['password']):
    return jsonify({'error': 'Invalid email or password'}), 401

  token = create_access_token(user.id, user.role)
  return jsonify({
    'message': 'Login successful',
    'token': token,
    'user': user.to_dict(),
  }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
  return jsonify({'message': 'Logged out successfully'}), 200
