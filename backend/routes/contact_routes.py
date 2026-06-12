from flask import Blueprint, request, jsonify
from models import db, Contact
from services.validation import (
  validate_required_fields,
  validate_email_address,
  validate_phone,
  validate_url,
  sanitize_string,
)
from services.email_service import send_contact_notification

contact_bp = Blueprint('contact', __name__, url_prefix='/api')


@contact_bp.route('/contact', methods=['POST'])
def submit_contact():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['name', 'email', 'message'])
  if not valid:
    return jsonify({'error': error}), 400

  name = sanitize_string(data['name'], 120)
  email = sanitize_string(data['email'], 255).lower()
  phone = sanitize_string(data.get('phone', ''), 30)
  website = sanitize_string(data.get('website', ''), 255)
  message = sanitize_string(data['message'], 5000)
  service = sanitize_string(data.get('service', ''), 100)

  valid_email, email_error = validate_email_address(email)
  if not valid_email:
    return jsonify({'error': email_error}), 400

  valid_phone, phone_error = validate_phone(phone)
  if not valid_phone:
    return jsonify({'error': phone_error}), 400

  valid_url, url_error = validate_url(website)
  if not valid_url:
    return jsonify({'error': url_error}), 400

  contact = Contact(
    name=name,
    email=email,
    phone=phone or None,
    website=website or None,
    message=message,
    service=service or None,
  )
  db.session.add(contact)
  db.session.commit()

  send_contact_notification(contact)

  return jsonify({
    'message': 'Contact form submitted successfully',
    'contact': contact.to_dict(),
  }), 201
