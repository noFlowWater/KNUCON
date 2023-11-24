from fastapi import FastAPI
from fastapi.security import HTTPBasic
from starlette.middleware.cors import CORSMiddleware

import domain.post.post_router as post_router

app = FastAPI()

origins=[
        "http://localhost:8000",       # FastAPI server url
        "http://127.0.0.1:8001",
        # "http://localhost:5173",       # Need Svelte(Frontend) server url
        # "http://155.230.36.27:5173",
        # "http://127.0.0.1:5173",
        ]  

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
allow_headers=["*"],
)

security = HTTPBasic()

app.include_router(post_router.router)
