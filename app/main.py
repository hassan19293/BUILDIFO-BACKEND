from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import router as api_router

app = FastAPI(title=settings.app_name, version="0.1.0")

allowed_origins = [
    "https://www.buildifo.com",
    "https://buildifo.com",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def get_root() -> dict[str, str]:
    return {"name": settings.app_name, "status": "ok"}