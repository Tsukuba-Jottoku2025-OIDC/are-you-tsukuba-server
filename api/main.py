from fastapi import FastAPI
from api.routers import protected

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

app.include_router(protected.router)
