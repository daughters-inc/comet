from fastapi import FastAPI
from src.comet import Comet

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Comet!"}


@app.get("/analyze/{video_id}")
async def analyze(video_id: str) -> dict:
    comet = Comet(video_id)
    return {"result": comet.analyze()}
