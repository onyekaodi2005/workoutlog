# FitLog

FitLog is a fullstack FastAPI app (no React) that demonstrates server-side rendering with Jinja2 plus HTMX for dynamic interactions.

Features:
- User registration/login (JWT in HttpOnly cookie)
- CRUD for workouts (date, activity, duration, notes)
- Server-side templates with partial updates via HTMX
- SQLite default, configurable DATABASE_URL

Quickstart:
1. Copy `.env.example` to `.env`
2. Run with Docker Compose: `docker-compose up --build`
3. Visit http://localhost:8000
