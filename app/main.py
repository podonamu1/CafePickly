# App 시작점
from fastapi import FastAPI
from app.api.routes import cafes

app = FastAPI(
    title="CafePickly",
    #version="0.1.0"
)

app.include_router(cafes.router)

@app.get("/")
def read_root():
    return {"message": "New CafePickly API"}