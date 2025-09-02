from fastapi import APIRouter, Request, Form, Depends, Response, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from app.db import engine
from app.models import User, Workout
from app.auth import hash_password, verify_password, create_token, decode_token

templates = Jinja2Templates(directory='templates')
router = APIRouter()

def get_user_by_email(email: str):
    with Session(engine) as s:
        stmt = select(User).where(User.email == email)
        return s.exec(stmt).first()

def get_current_user(request: Request):
    token = request.cookies.get('access_token')
    if not token:
        return None
    email = decode_token(token)
    if not email:
        return None
    return get_user_by_email(email)

@router.get('/', response_class=HTMLResponse)
async def index(request: Request):
    user = get_current_user(request)
    with Session(engine) as s:
        workouts = []
        if user:
            stmt = select(Workout).where(Workout.owner_id == user.id).order_by(Workout.date.desc())
            workouts = s.exec(stmt).all()
    return templates.TemplateResponse('index.html', {'request': request, 'user': user, 'workouts': workouts})

@router.post('/register')
async def register(request: Request, email: str = Form(...), password: str = Form(...)):
    if get_user_by_email(email):
        return templates.TemplateResponse('register.html', {'request': request, 'error': 'Email exists'}, status_code=400)
    user = User(email=email, hashed_password=hash_password(password))
    with Session(engine) as s:
        s.add(user); s.commit(); s.refresh(user)
    response = RedirectResponse('/', status_code=303)
    token = create_token(user.email)
    response.set_cookie('access_token', token, httponly=True)
    return response

@router.get('/register', response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse('register.html', {'request': request})

@router.post('/login')
async def login(request: Request, email: str = Form(...), password: str = Form(...)):
    user = get_user_by_email(email)
    if not user or not verify_password(password, user.hashed_password):
        return templates.TemplateResponse('login.html', {'request': request, 'error': 'Invalid credentials'}, status_code=400)
    response = RedirectResponse('/', status_code=303)
    token = create_token(user.email)
    response.set_cookie('access_token', token, httponly=True)
    return response

@router.get('/login', response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})

@router.post('/logout')
async def logout():
    response = RedirectResponse('/', status_code=303)
    response.delete_cookie('access_token')
    return response

@router.post('/workouts', response_class=HTMLResponse)
async def add_workout(request: Request, date: str = Form(...), activity: str = Form(...), duration_minutes: int = Form(...), notes: str = Form(None)):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail='Not authenticated')
    workout = Workout(owner_id=user.id, date=date, activity=activity, duration_minutes=duration_minutes, notes=notes)
    with Session(engine) as s:
        s.add(workout); s.commit(); s.refresh(workout)
    if request.headers.get('hx-request'):
        return templates.TemplateResponse('_workout_item.html', {'request': request, 'w': workout})
    return RedirectResponse('/', status_code=303)

@router.post('/workouts/delete/{wid}')
async def delete_workout(request: Request, wid: int):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail='Not authenticated')
    with Session(engine) as s:
        w = s.get(Workout, wid)
        if not w or w.owner_id != user.id:
            raise HTTPException(status_code=404, detail='Not found')
        s.delete(w); s.commit()
    if request.headers.get('hx-request'):
        return Response(content='OK')
    return RedirectResponse('/', status_code=303)
