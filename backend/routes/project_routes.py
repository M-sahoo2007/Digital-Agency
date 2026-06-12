from flask import Blueprint, request, jsonify
from models import db, Project
from auth.decorators import admin_required
from services.validation import validate_required_fields, sanitize_string

project_bp = Blueprint('projects', __name__, url_prefix='/api/projects')


@project_bp.route('', methods=['GET'])
def get_projects():
  category = request.args.get('category', '', type=str).strip()
  query = Project.query.order_by(Project.id.desc())

  if category and category.lower() != 'all':
    query = query.filter(Project.category.ilike(category))

  projects = query.all()
  return jsonify({'projects': [project.to_dict() for project in projects]}), 200


@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
  project = db.session.get(Project, project_id)
  if not project:
    return jsonify({'error': 'Project not found'}), 404
  return jsonify(project.to_dict()), 200


@project_bp.route('', methods=['POST'])
@admin_required
def create_project():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['title', 'category', 'image'])
  if not valid:
    return jsonify({'error': error}), 400

  project = Project(
    title=sanitize_string(data['title'], 200),
    category=sanitize_string(data['category'], 100),
    image=sanitize_string(data['image'], 500),
    description=sanitize_string(data.get('description', ''), 5000) or None,
    date=sanitize_string(data.get('date', ''), 50) or None,
  )
  db.session.add(project)
  db.session.commit()

  return jsonify({'message': 'Project created', 'project': project.to_dict()}), 201


@project_bp.route('/<int:project_id>', methods=['PUT'])
@admin_required
def update_project(project_id):
  project = db.session.get(Project, project_id)
  if not project:
    return jsonify({'error': 'Project not found'}), 404

  data = request.get_json(silent=True) or {}

  if 'title' in data:
    project.title = sanitize_string(data['title'], 200)
  if 'category' in data:
    project.category = sanitize_string(data['category'], 100)
  if 'image' in data:
    project.image = sanitize_string(data['image'], 500)
  if 'description' in data:
    project.description = sanitize_string(data['description'], 5000) or None
  if 'date' in data:
    project.date = sanitize_string(data['date'], 50) or None

  db.session.commit()
  return jsonify({'message': 'Project updated', 'project': project.to_dict()}), 200


@project_bp.route('/<int:project_id>', methods=['DELETE'])
@admin_required
def delete_project(project_id):
  project = db.session.get(Project, project_id)
  if not project:
    return jsonify({'error': 'Project not found'}), 404

  db.session.delete(project)
  db.session.commit()
  return jsonify({'message': 'Project deleted'}), 200
