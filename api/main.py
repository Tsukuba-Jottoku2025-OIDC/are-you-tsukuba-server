
from datetime import date
# from api import errors
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# from api.errors import ApiError
from api.routers import me

from dotenv import load_dotenv

load_dotenv()

tags_metadata = [
    {
        "name": "health",
        "description": "APIの死活状態に関するエンドポイント",
    },
]

app = FastAPI(openapi_tags=tags_metadata)

origins = [
    # os.environ["APP_FRONTEND_ENDPOINT"],
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="http://localhost:.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello_world():
    return {"message": "OK"}


# @app.exception_handler(ApiError)
# async def api_error_handler(request, err: ApiError):
    raise HTTPException(status_code=err.status_code, detail={"message": err.message})


# app.include_router(me.router)
