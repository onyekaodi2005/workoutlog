# WorkoutLog

workoutlog is a fullstack FastAPI app (no React) that demonstrates server-side rendering with Jinja2 plus HTMX for dynamic interactions.

Features:
- User registration/login (JWT in HttpOnly cookie)
- CRUD for workouts (date, activity, duration, notes)
- Server-side templates with partial updates via HTMX
- SQLite default, configurable DATABASE_URL

Quickstart:
1. Run with Docker Compose: `docker-compose up --build` or `uvicorn app.main:app --reload`
2. Visit http://localhost:8000

Python Version: 3.13.6