from fastapi import FastAPI
from fastapi.security import HTTPBasic
from starlette.middleware.cors import CORSMiddleware

# test
import domain.user.user_router as user_router
# import domain.connection.connection_router as connection_router
# import domain.app.app_router as app_router
# import domain.volume.volume_router as volume_router
# import domain.apprun.apprun_router as apprun_router

app = FastAPI()

origins=[
        "http://localhost:8000",       # FastAPI server url
        "http://155.230.36.27:8000",
        "http://127.0.0.1:8000",
        "http://localhost:5173",       # Svelte(Frontend) server url
        "http://155.230.36.27:5173",
        "http://127.0.0.1:5173",
        ]  

app.add_middleware(
CORSMiddleware,
allow_origins=origins,
allow_credentials=True,
allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
allow_headers=["*"],
)

security = HTTPBasic()

app.include_router(user_router.router)