from fastapi import FastAPI
from api.routers.auth import router as auth_router
from api.routers.protected import router as protected_router

app = FastAPI(title="are-you-tsukuba-server")

app.include_router(auth_router)
app.include_router(protected_router)

@app.get("/health")
def health():
    return {"status": "ok"}
