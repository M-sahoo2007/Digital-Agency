import os
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
from flask_mail import Mail
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from config import Config
from models import db, User, Project, Blog
from routes.auth_routes import auth_bp
from routes.contact_routes import contact_bp
from routes.newsletter_routes import newsletter_bp
from routes.blog_routes import blog_bp
from routes.project_routes import project_bp
from routes.admin_routes import admin_bp

mail = Mail()
migrate = Migrate()
limiter = Limiter(key_func=get_remote_address)


def create_app(config_class=Config):
  app = Flask(__name__)
  app.config.from_object(config_class)

  db.init_app(app)
  mail.init_app(app)
  migrate.init_app(app, db)
  limiter.init_app(app)

  CORS(
    app,
    origins=app.config['CORS_ORIGINS'],
    supports_credentials=True,
    allow_headers=['Content-Type', 'Authorization'],
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
  )

  app.register_blueprint(auth_bp)
  app.register_blueprint(contact_bp)
  app.register_blueprint(newsletter_bp)
  app.register_blueprint(blog_bp)
  app.register_blueprint(project_bp)
  app.register_blueprint(admin_bp)

  limiter.limit('10 per minute')(app.view_functions['contact.submit_contact'])
  limiter.limit('5 per minute')(app.view_functions['newsletter.subscribe'])
  limiter.limit('5 per minute')(app.view_functions['auth.login'])
  limiter.limit('3 per minute')(app.view_functions['auth.register'])

  frontend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend')

  @app.route('/api/health')
  def health():
    return jsonify({'status': 'ok', 'service': 'M-sahoo2007 API'}), 200

  @app.route('/')
  def serve_index():
    return send_from_directory(frontend_path, 'index.html')

  @app.route('/admin')
  @app.route('/admin/')
  def serve_admin():
    return send_from_directory(frontend_path, 'admin.html')

  @app.route('/<path:filename>')
  def serve_frontend(filename):
    if filename.startswith('api/'):
      return jsonify({'error': 'Not found'}), 404
    file_path = os.path.join(frontend_path, filename)
    if os.path.exists(file_path):
      return send_from_directory(frontend_path, filename)
    return send_from_directory(frontend_path, 'index.html')

  @app.cli.command('seed')
  def seed_data():
    seed_database()

  return app


def seed_database():
  if Project.query.count() == 0:
    projects = [
      Project(
        title='Finance Management System',
        category='App Design',
        image='assets/images/project-1.svg',
        description='A comprehensive finance management platform with real-time analytics and budgeting tools.',
        date='2025',
      ),
      Project(
        title='SaaS Dashboard UI',
        category='SaaS',
        image='assets/images/project-2.svg',
        description='Modern SaaS dashboard with intuitive data visualization and user management.',
        date='2025',
      ),
      Project(
        title='Crypto Trading Platform',
        category='SaaS',
        image='assets/images/project-3.svg',
        description='High-performance crypto trading interface with live market data.',
        date='2024',
      ),
      Project(
        title='E-commerce Redesign',
        category='Webflow Development',
        image='assets/images/project-4.svg',
        description='Complete e-commerce redesign focused on conversion and user experience.',
        date='2024',
      ),
      Project(
        title='Health & Fitness App',
        category='App Design',
        image='assets/images/project-5.svg',
        description='Mobile-first fitness tracking app with personalized workout plans.',
        date='2024',
      ),
      Project(
        title='Real Estate Portal',
        category='Webflow Development',
        image='assets/images/project-6.svg',
        description='Property listing platform with advanced search and virtual tours.',
        date='2023',
      ),
      Project(
        title='Banking App Interaction',
        category='App Design',
        image='assets/images/project-7.svg',
        description='Next-gen banking app with seamless micro-interactions and security.',
        date='2023',
      ),
      Project(
        title='Analytics Dashboard',
        category='SaaS',
        image='assets/images/project-8.svg',
        description='Enterprise analytics dashboard with customizable widgets and reports.',
        date='2023',
      ),
    ]
    db.session.add_all(projects)

  if Blog.query.count() == 0:
    blogs = [
      Blog(
        title='The Future of Digital Product Design in 2026',
        slug='future-digital-product-design-2026',
        image='assets/images/blog-1.svg',
        category='Design',
        content='Digital product design continues to evolve with AI-assisted workflows, immersive interfaces, and human-centered methodologies. At M-sahoo2007, we believe the future lies in blending cutting-edge technology with timeless design principles to create products that truly resonate with users.',
      ),
      Blog(
        title='Building Scalable SaaS Applications',
        slug='building-scalable-saas-applications',
        image='assets/images/blog-2.svg',
        category='Development',
        content='Scalability is not an afterthought—it is a foundation. From microservices architecture to cloud-native deployments, we explore the strategies that help SaaS products grow from MVP to enterprise-grade solutions without compromising performance.',
      ),
      Blog(
        title='Why Minimal Design Drives Conversion',
        slug='minimal-design-drives-conversion',
        image='assets/images/blog-3.svg',
        category='Strategy',
        content='Less is more when it comes to conversion-focused design. We break down how minimalist interfaces reduce cognitive load, improve user flow, and ultimately drive higher engagement and revenue for digital products.',
      ),
      Blog(
        title='Mobile-First Development Best Practices',
        slug='mobile-first-development-best-practices',
        image='assets/images/blog-4.svg',
        category='Development',
        content='With mobile traffic dominating the web, adopting a mobile-first approach is essential. Learn the best practices for responsive design, touch interactions, and performance optimization that we apply to every project.',
      ),
      Blog(
        title='The Role of AI in Creative Agencies',
        slug='role-of-ai-in-creative-agencies',
        image='assets/images/blog-5.svg',
        category='Innovation',
        content='AI is transforming how creative agencies work—from automated design systems to intelligent content generation. Discover how M-sahoo2007 leverages AI to enhance creativity while maintaining the human touch that defines great design.',
      ),
      Blog(
        title='Webflow vs Custom Development',
        slug='webflow-vs-custom-development',
        image='assets/images/blog-6.svg',
        category='Strategy',
        content='Choosing between Webflow and custom development depends on your project goals, budget, and timeline. We compare both approaches to help you make an informed decision for your next digital product.',
      ),
    ]
    db.session.add_all(blogs)

  if User.query.filter_by(role='admin').count() == 0:
    admin = User(name='Admin', email='admin@m-sahoo2007.com', role='admin')
    admin.set_password('Admin@12345')
    db.session.add(admin)

  db.session.commit()
  print('Database seeded successfully.')


# app = create_app()

# if __name__ == '__main__':
#   with app.app_context():
#     try:
#       db.create_all()
#       seed_database()
#       print(f'Database ready: {app.config["SQLALCHEMY_DATABASE_URI"]}')
#     except Exception as exc:
#       print(f'Database setup failed: {exc}')
#       print('If using PostgreSQL, ensure the server is running and DATABASE_URL is correct.')
#       raise
#   app.run(debug=True, host='0.0.0.0', port=5000)

# app = create_app()

# with app.app_context():
#     db.create_all()
#     seed_database()

app = create_app()

with app.app_context():
    try:
        db.create_all()
        seed_database()
        print("Database initialized")
    except Exception as exc:
        print(f"Database error: {exc}")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)