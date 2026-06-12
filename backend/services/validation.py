import re
from email_validator import validate_email, EmailNotValidError


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
PHONE_REGEX = re.compile(r'^[\d\s\-\+\(\)]{7,20}$')
URL_REGEX = re.compile(r'^https?://[^\s/$.?#].[^\s]*$', re.IGNORECASE)


def validate_required_fields(data, fields):
  missing = [field for field in fields if not data.get(field) or not str(data.get(field)).strip()]
  if missing:
    return False, f"Missing required fields: {', '.join(missing)}"
  return True, None


def validate_email_address(email):
  try:
    validate_email(email, check_deliverability=False)
    return True, None
  except EmailNotValidError as exc:
    return False, str(exc)


def validate_phone(phone):
  if not phone:
    return True, None
  if not PHONE_REGEX.match(phone.strip()):
    return False, 'Invalid phone number format'
  return True, None


def validate_url(url):
  if not url:
    return True, None
  if not URL_REGEX.match(url.strip()):
    return False, 'Invalid website URL'
  return True, None


def sanitize_string(value, max_length=500):
  if value is None:
    return ''
  return str(value).strip()[:max_length]
