from flask import Blueprint, request, jsonify
from models import db, Blog
from auth.decorators import admin_required
from services.validation import validate_required_fields, sanitize_string

blog_bp = Blueprint('blogs', __name__, url_prefix='/api/blogs')


@blog_bp.route('', methods=['GET'])
def get_blogs():
  page = request.args.get('page', 1, type=int)
  per_page = request.args.get('per_page', 6, type=int)
  search = request.args.get('search', '', type=str).strip()
  category = request.args.get('category', '', type=str).strip()

  query = Blog.query.order_by(Blog.created_at.desc())

  if search:
    query = query.filter(Blog.title.ilike(f'%{search}%'))
  if category and category.lower() != 'all':
    query = query.filter(Blog.category.ilike(category))

  pagination = query.paginate(page=page, per_page=per_page, error_out=False)

  return jsonify({
    'blogs': [blog.to_dict() for blog in pagination.items],
    'total': pagination.total,
    'page': pagination.page,
    'pages': pagination.pages,
    'per_page': pagination.per_page,
  }), 200


@blog_bp.route('/<int:blog_id>', methods=['GET'])
def get_blog(blog_id):
  blog = db.session.get(Blog, blog_id)
  if not blog:
    return jsonify({'error': 'Blog not found'}), 404
  return jsonify(blog.to_dict(include_content=True)), 200


@blog_bp.route('', methods=['POST'])
@admin_required
def create_blog():
  data = request.get_json(silent=True) or {}
  valid, error = validate_required_fields(data, ['title', 'image', 'content', 'category'])
  if not valid:
    return jsonify({'error': error}), 400

  title = sanitize_string(data['title'], 255)
  slug = data.get('slug') or Blog.slugify(title)

  if Blog.query.filter_by(slug=slug).first():
    slug = f"{slug}-{Blog.query.count() + 1}"

  blog = Blog(
    title=title,
    slug=slug,
    image=sanitize_string(data['image'], 500),
    content=sanitize_string(data['content'], 50000),
    category=sanitize_string(data['category'], 100),
  )
  db.session.add(blog)
  db.session.commit()

  return jsonify({'message': 'Blog created', 'blog': blog.to_dict(include_content=True)}), 201


@blog_bp.route('/<int:blog_id>', methods=['PUT'])
@admin_required
def update_blog(blog_id):
  blog = db.session.get(Blog, blog_id)
  if not blog:
    return jsonify({'error': 'Blog not found'}), 404

  data = request.get_json(silent=True) or {}

  if 'title' in data:
    blog.title = sanitize_string(data['title'], 255)
  if 'slug' in data:
    blog.slug = sanitize_string(data['slug'], 255)
  if 'image' in data:
    blog.image = sanitize_string(data['image'], 500)
  if 'content' in data:
    blog.content = sanitize_string(data['content'], 50000)
  if 'category' in data:
    blog.category = sanitize_string(data['category'], 100)

  db.session.commit()
  return jsonify({'message': 'Blog updated', 'blog': blog.to_dict(include_content=True)}), 200


@blog_bp.route('/<int:blog_id>', methods=['DELETE'])
@admin_required
def delete_blog(blog_id):
  blog = db.session.get(Blog, blog_id)
  if not blog:
    return jsonify({'error': 'Blog not found'}), 404

  db.session.delete(blog)
  db.session.commit()
  return jsonify({'message': 'Blog deleted'}), 200
