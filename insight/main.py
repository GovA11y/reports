# main.py
# Relative Path: insight/main.py
from fastapi import FastAPI
from .api import routes

app = FastAPI()

app.include_router(routes.router)