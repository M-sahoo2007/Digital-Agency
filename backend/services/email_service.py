from flask import current_app
from flask_mail import Message
from models import db


def get_mail():
  from app import mail
  return mail


def send_contact_notification(contact):
  mail = get_mail()
  if not current_app.config.get('MAIL_USERNAME'):
    return False

  subject = f'New Contact Inquiry from {contact.name}'
  body = f"""
New contact form submission:

Name: {contact.name}
Email: {contact.email}
Phone: {contact.phone or 'N/A'}
Website: {contact.website or 'N/A'}
Service: {contact.service or 'N/A'}

Message:
{contact.message}
"""

  msg = Message(
    subject=subject,
    recipients=[current_app.config['ADMIN_EMAIL']],
    body=body,
  )

  try:
    mail.send(msg)
    return True
  except Exception:
    return False
