# Intelligent Career Planner

A web platform to organize your professional development — studies, projects, certifications and career goals — all in one place.

## Overview

This project was born from the need to organize information related to professional development, centralizing studies, projects, certifications and goals in a single place.

The goal is to provide a base that can be used and adapted by any technology professional — whether you are an RPA Developer, Data Analyst, AI Engineer, IT Governance specialist, infrastructure engineer, or student.

## Features

- **Task Planner** — Create and track study goals with area, priority, deadlines and time estimates
- **Weekly Review** — Plan your week with focused tasks and daily logging
- **Project Management** — Track personal and corporate projects with progress, tech stack, evidence links and FTE metrics
- **Skills Dashboard** — Organize technical competencies by category (RPA, Cloud, AI, Integrations, etc.)
- **Certificate Manager** — Log certifications with issuer, dates, credential IDs and LinkedIn validation links
- **Resume Generator** — Auto-generated resume page (HTML + PDF) pulling data from the database and `data/resume.json`
- **Admin Mode** — Login-protected editing with a viewer/recruiter mode that hides sensitive data (LGPD/NDA)
- **Backup & Restore** — Export/import all data as JSON

## Technologies

| Layer | Stack |
|-------|-------|
| Backend | Python 3.11+, Flask 3, Flask-SQLAlchemy, Flask-Migrate |
| Database | SQLite (file-based, zero config) |
| Frontend | Jinja2 templates, vanilla CSS, vanilla JS |
| PDF | WeasyPrint (optional, falls back to browser print) |
| Hosting | Render (or any WSGI host) |
| Server | Gunicorn |

## Installation

```bash
# Clone the repository
git clone https://github.com/your-username/intelligent-career-planner.git
cd intelligent-career-planner

# Create a virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run the application
python app.py
```

The app starts at `http://localhost:5000`. On first run, the database is created automatically with demo data.

### Admin Access

Navigate to `/admin?key=admin2026` to enable admin mode (edit, add, delete data).

Set the `ADMIN_KEY` environment variable to change the default key:

```bash
export ADMIN_KEY=your-secret-key
```

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-change-me` | Flask session secret |
| `ADMIN_KEY` | `admin2026` | Admin login key |
| `DATABASE_URL` | `sqlite:///data/app.db` | Database URI |

## Project Structure

```
intelligent-career-planner/
├── app/
│   ├── __init__.py        # Application factory + seed data
│   ├── config.py          # Configuration (env vars, paths)
│   ├── models.py          # SQLAlchemy models (Task, Project, SkillCategory, Certificate)
│   └── routes.py          # All routes, CRUD logic, stats computation
├── templates/             # Jinja2 HTML templates
│   ├── base.html          # Layout with navbar, tabs, footer
│   ├── about.html         # Welcome / dashboard page
│   ├── planner.html       # Task planner
│   ├── weekly.html        # Weekly review
│   ├── projects.html      # Project list + add form
│   ├── project_detail.html # Project detail with evidence
│   ├── skills.html        # Skills dashboard
│   ├── certificates.html  # Certificate manager
│   ├── resume.html        # Resume / CV page
│   └── edit_*.html        # Edit forms
├── static/
│   ├── css/styles.css     # Full design system (dark theme)
│   └── js/main.js         # Client-side interactions
├── data/
│   ├── app.db             # SQLite database (auto-created)
│   └── resume.json        # Extra resume data (experience, education)
├── app.py                 # Development entry point
├── wsgi.py                # Production entry point (Gunicorn)
├── render.yaml            # Render.com deploy config
└── requirements.txt       # Python dependencies
```

## Customization

### Your Resume Data

Edit `data/resume.json` with your personal information:

```json
{
  "name": "Your Name",
  "headline": "Your Title | Your Specialty",
  "location": "City, Country",
  "email": "your@email.com",
  "linkedin": "https://linkedin.com/in/yourprofile",
  "summary": "Your professional summary...",
  "keywords": ["Python", "RPA", "AI"],
  "experience": [...],
  "education": [...]
}
```

### Skills Categories

Add skill categories via the admin UI or edit the seed data in `app/__init__.py`.

### Branding

Update `templates/base.html` to change the app name and tagline.

## Roadmap

- [ ] Dark/light theme toggle
- [ ] Multi-language support (i18n)
- [ ] Dashboard charts (progress over time)
- [ ] Export resume to DOCX
- [ ] API endpoints for external integrations
- [ ] User registration (multi-tenant)
- [ ] Mobile-responsive improvements
- [ ] Notification system for deadlines

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
