from flask import Blueprint, jsonify
from models import Contact, Newsletter, User, Project, Blog
from auth.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')


@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
  return jsonify({
    'contacts': Contact.query.count(),
    'newsletter': Newsletter.query.count(),
    'projects': Project.query.count(),
    'blogs': Blog.query.count(),
    'users': User.query.count(),
  }), 200


@admin_bp.route('/contacts', methods=['GET'])
@admin_required
def get_contacts():
  contacts = Contact.query.order_by(Contact.created_at.desc()).limit(50).all()
  return jsonify({'contacts': [c.to_dict() for c in contacts]}), 200
