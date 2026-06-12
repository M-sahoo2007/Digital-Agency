from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import re

db = SQLAlchemy()


def utcnow():
  return datetime.now(timezone.utc)


class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(255), unique=True, nullable=False, index=True)
  password_hash = db.Column(db.String(255), nullable=False)
  role = db.Column(db.String(20), nullable=False, default='user')
  created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

  def set_password(self, password):
    self.password_hash = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def is_admin(self):
    return self.role == 'admin'

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'role': self.role,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }


class Contact(db.Model):
  __tablename__ = 'contacts'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(120), nullable=False)
  email = db.Column(db.String(255), nullable=False)
  phone = db.Column(db.String(30), nullable=True)
  website = db.Column(db.String(255), nullable=True)
  message = db.Column(db.Text, nullable=False)
  service = db.Column(db.String(100), nullable=True)
  created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

  def to_dict(self):
    return {
      'id': self.id,
      'name': self.name,
      'email': self.email,
      'phone': self.phone,
      'website': self.website,
      'message': self.message,
      'service': self.service,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }


class Project(db.Model):
  __tablename__ = 'projects'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  category = db.Column(db.String(100), nullable=False, index=True)
  image = db.Column(db.String(500), nullable=False)
  description = db.Column(db.Text, nullable=True)
  date = db.Column(db.String(50), nullable=True)

  def to_dict(self):
    return {
      'id': self.id,
      'title': self.title,
      'category': self.category,
      'image': self.image,
      'description': self.description,
      'date': self.date,
    }


class Blog(db.Model):
  __tablename__ = 'blogs'

  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(255), nullable=False)
  slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
  image = db.Column(db.String(500), nullable=False)
  content = db.Column(db.Text, nullable=False)
  category = db.Column(db.String(100), nullable=False, index=True)
  created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

  @staticmethod
  def slugify(title):
    slug = re.sub(r'[^\w\s-]', '', title.lower())
    slug = re.sub(r'[\s_-]+', '-', slug).strip('-')
    return slug

  def to_dict(self, include_content=False):
    data = {
      'id': self.id,
      'title': self.title,
      'slug': self.slug,
      'image': self.image,
      'category': self.category,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }
    if include_content:
      data['content'] = self.content
    return data


class Newsletter(db.Model):
  __tablename__ = 'newsletter'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(255), unique=True, nullable=False, index=True)
  created_at = db.Column(db.DateTime(timezone=True), default=utcnow, nullable=False)

  def to_dict(self):
    return {
      'id': self.id,
      'email': self.email,
      'created_at': self.created_at.isoformat() if self.created_at else None,
    }
