# App 시작점
from fastapi import FastAPI
from fastapi.middleware.cors import  CORSMiddleware

from app.db.session import engine
from app.db.base import Base
from app.api.routes import cafes

app = FastAPI(
    title="CafePickly",
    #version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(cafes.router)

@app.get("/")
def read_root():
    return {"message": "New CafePickly API"}