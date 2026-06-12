from flask import Blueprint, request, jsonify
from models import db, Newsletter
from services.validation import validate_required_fields, validate_email_address, sanitize_string

newsletter_bp = Blueprint('newsletter', __name__, url_prefix='/api')


@newsletter_bp.route('/newsletter', methods=['POST'])
def subscribe():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['email'])
  if not valid:
    return jsonify({'error': error}), 400

  email = sanitize_string(data['email'], 255).lower()
  valid_email, email_error = validate_email_address(email)
  if not valid_email:
    return jsonify({'error': email_error}), 400

  existing = Newsletter.query.filter_by(email=email).first()
  if existing:
    return jsonify({'message': 'Already subscribed', 'subscriber': existing.to_dict()}), 200

  subscriber = Newsletter(email=email)
  db.session.add(subscriber)
  db.session.commit()

  return jsonify({
    'message': 'Successfully subscribed to newsletter',
    'subscriber': subscriber.to_dict(),
  }), 201
