# M-sahoo2007 — Premium Digital Agency Website

A full-stack production-ready creative agency website with a luxury monochrome design, GSAP animations, Lenis smooth scroll, Swiper.js testimonials, and a Flask REST API backend with PostgreSQL / SQLite.

---

## Complete Project Structure

```
m-sahoo2007/
│
├── README.md
│
├── frontend/
│   ├── index.html              # Home page — hero, partners, about, services, team, testimonials
│   ├── about.html              # About page — story, stats, values, team
│   ├── projects.html           # Projects portfolio with category filters
│   ├── blog.html               # Blog listing with search, filter, pagination
│   ├── contact.html            # Contact form + interactive calendar
│   ├── admin.html              # Admin login + dashboard
│   ├── robots.txt              # Search engine crawler rules
│   ├── sitemap.xml             # SEO sitemap
│   │
│   ├── css/
│   │   ├── style.css           # Core design system and component styles
│   │   ├── responsive.css      # Breakpoints: 1440 / 1280 / 768 / 375
│   │   └── animations.css      # GSAP helpers, loaders, hover utilities
│   │
│   ├── js/
│   │   ├── app.js              # Navbar, Lenis, filters, contact form, calendar
│   │   ├── gsap.js             # Scroll animations, counters, magnetic buttons
│   │   ├── swiper.js           # Testimonials slider
│   │   └── api.js              # REST API client (JWT, contact, blogs, projects)
│   │
│   └── assets/
│       ├── images/
│       │   ├── project-1.svg   # Finance Management System
│       │   ├── project-2.svg   # SaaS Dashboard UI
│       │   ├── project-3.svg   # Crypto Trading Platform
│       │   ├── project-4.svg   # E-commerce Redesign
│       │   ├── project-5.svg   # Health & Fitness App
│       │   ├── project-6.svg   # Real Estate Portal
│       │   ├── project-7.svg   # Banking App Interaction
│       │   ├── project-8.svg   # Analytics Dashboard
│       │   ├── blog-1.svg      # Blog cover images (6 posts)
│       │   ├── blog-2.svg
│       │   ├── blog-3.svg
│       │   ├── blog-4.svg
│       │   ├── blog-5.svg
│       │   ├── blog-6.svg
│       │   ├── team-1.svg      # Alex Morgan — CEO & Founder
│       │   ├── team-2.svg      # Sarah Chen — Creative Director
│       │   ├── team-3.svg      # Marcus Rivera — Lead Developer
│       │   └── team-4.svg      # Elena Vasquez — UX Strategist
│       ├── icons/              # Icon assets directory
│       └── videos/             # Video assets directory
│
├── backend/
│   ├── app.py                  # Flask app factory, routes, seed command
│   ├── config.py               # Environment config, SQLite / PostgreSQL URI
│   ├── models.py               # SQLAlchemy models (User, Contact, Project, Blog, Newsletter)
│   ├── requirements.txt        # Python dependencies
│   ├── .env                    # Local environment variables (not committed)
│   ├── .env.example            # Environment template
│   │
│   ├── auth/ 
│   │   ├── __init__.py
│   │   ├── jwt_handler.py      # JWT token create / decode
│   │   └── decorators.py       # @token_required, @admin_required
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py      # POST /api/auth/register, login, logout
│   │   ├── contact_routes.py   # POST /api/contact
│   │   ├── newsletter_routes.py# POST /api/newsletter
│   │   ├── blog_routes.py      # CRUD /api/blogs
│   │   └── project_routes.py   # CRUD /api/projects
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── email_service.py    # Flask-Mail contact notifications
│   │   └── validation.py       # Input validation and sanitization
│   │
│   └── migrations/             # Alembic / Flask-Migrate (PostgreSQL)
│       ├── alembic.ini
│       ├── env.py
│       ├── README
│       └── script.py.mako
│
└── database/
    └── m_sahoo2007.db            # SQLite database (local dev, auto-created)
```

---

## File Summary

| Category | Count | Files |
|----------|-------|-------|
| HTML pages | 5 | `index.html`, `about.html`, `projects.html`, `blog.html`, `contact.html` |
| CSS | 3 | `style.css`, `responsive.css`, `animations.css` |
| JavaScript | 4 | `app.js`, `gsap.js`, `swiper.js`, `api.js` |
| Images (SVG) | 18 | 8 projects, 6 blogs, 4 team |
| Backend Python | 14 | `app.py`, `config.py`, `models.py`, routes, auth, services |
| Config | 2 | `.env`, `.env.example` |
| SEO | 2 | `robots.txt`, `sitemap.xml` |
| Database | 1 | `m_sahoo2007.db` |

---

## Prerequisites

- Python 3.10+
- PostgreSQL 14+ (optional — SQLite used by default for local dev)
- Node.js (optional, for Live Server)

---

## Backend Setup

### 1. Install dependencies

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
# Edit .env with your database and mail credentials
```

### 3. Run the server

```bash
python app.py
```

- **Website:** http://localhost:5000
- **API:** http://localhost:5000/api
- **Health check:** http://localhost:5000/api/health
- **Admin panel:** http://localhost:5000/admin

Local dev uses **SQLite** by default (`database/m_sahoo2007.db`). Tables and seed data are created automatically on first run.

**Default admin:** `admin@m-sahoo2007.com` / `Admin@12345`

> Use `http://127.0.0.1:5000` or `http://localhost:5000` — not `/index.html/admin`. The API uses same-origin requests automatically.

---

## PostgreSQL (Production)

1. Create database:

```sql
CREATE DATABASE m_sahoo2007;
```

2. In `.env` set:

```
USE_SQLITE=false
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/m_sahoo2007
```

3. Initialize migrations (PowerShell):

```powershell
$env:FLASK_APP="app.py"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask seed
```

4. Run:

```bash
python app.py
```

---

## Frontend Setup

### Option A: Served by Flask (recommended)

Run `python app.py` — Flask serves all frontend files at `http://localhost:5000`

### Option B: Live Server

Open `frontend/index.html` with Live Server. API calls default to `http://localhost:5000/api`.

---

## API Endpoints

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/api/health` | No | Health check |
| GET | `/api/admin/stats` | Admin | Dashboard statistics |
| GET | `/api/admin/contacts` | Admin | List contact submissions |
| POST | `/api/auth/register` | No | Register user |
| POST | `/api/auth/login` | No | Login, get JWT |
| POST | `/api/auth/logout` | No | Logout |
| POST | `/api/contact` | No | Submit contact form |
| POST | `/api/newsletter` | No | Subscribe newsletter |
| GET | `/api/blogs` | No | List blogs (search, filter, pagination) |
| GET | `/api/blogs/:id` | No | Get blog by ID |
| POST | `/api/blogs` | Admin | Create blog |
| PUT | `/api/blogs/:id` | Admin | Update blog |
| DELETE | `/api/blogs/:id` | Admin | Delete blog |
| GET | `/api/projects` | No | List projects |
| GET | `/api/projects/:id` | No | Get project |
| POST | `/api/projects` | Admin | Create project |
| PUT | `/api/projects/:id` | Admin | Update project |
| DELETE | `/api/projects/:id` | Admin | Delete project |

---

## Database Tables

| Table | Columns |
|-------|---------|
| **users** | id, name, email, password_hash, role, created_at |
| **contacts** | id, name, email, phone, website, message, service, created_at |
| **projects** | id, title, category, image, description, date |
| **blogs** | id, title, slug, image, content, category, created_at |
| **newsletter** | id, email, created_at |

---

## Tech Stack

**Frontend:** HTML5, CSS3, Vanilla JavaScript, GSAP, Lenis, Swiper.js

**Backend:** Python, Flask, PostgreSQL / SQLite, SQLAlchemy, Flask-Migrate, Flask-Mail, JWT

**Security:** Password hashing, JWT auth, input validation, rate limiting, CORS

**SEO:** Meta tags, Open Graph, Twitter Cards, Schema.org, sitemap, robots.txt

---

## Design System

| Token | Value |
|-------|-------|
| Background | `#F5F5F5` |
| Black | `#000000` |
| Dark | `#111111` |
| Border | `#E5E5E5` |
| Text Gray | `#666666` |
| White | `#FFFFFF` |
| Border Radius | `24px` |
| Container | `1440px` |
| Font | General Sans, Inter, Satoshi |

---

## License

Proprietary — M-sahoo2007 © 2026
