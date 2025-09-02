from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.db import init_db
import sys, os
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from app.api import web


app = FastAPI(title='FitLog')

app.mount('/static', StaticFiles(directory='static'), name='static')

@app.on_event('startup')
async def startup():
    await init_db()

app.include_router(web.router)
