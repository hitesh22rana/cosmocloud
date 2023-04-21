from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from .routers import users, organizations
from .database import connect_to_db

"""FastAPI Instance"""
app = FastAPI()

"""MiddleWare"""
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*']
)

"""All the Routes"""
app.include_router(users.router)
app.include_router(organizations.router)

"""Database Connection"""
@app.on_event("startup")
async def startup_db_client():
    await connect_to_db()

"""GET Method - Root"""
@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')