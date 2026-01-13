from fastapi import FastAPI

from api.routers import auth, protected

app = FastAPI(title="are-you-tsukuba-server")

# 任意（dev login）
app.include_router(auth.router)

# 保護API
app.include_router(protected.router)


@app.get("/health")
def health():
    return {"status": "ok"}
