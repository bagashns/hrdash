"""
HRDash — FastAPI entry point (Minggu 1).

Menjalankan API CV Parser dan menyajikan halaman frontend statis.
"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .api.upload import router as upload_router


BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


app = FastAPI(
    title="HRDash API",
    description="AI-Based CV Screening Platform — MVP Minggu 1",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload_router, prefix="/api")


# ===== Sajikan frontend statis =====
if FRONTEND_DIR.exists():
    app.mount(
        "/assets",
        StaticFiles(directory=FRONTEND_DIR / "assets"),
        name="assets",
    )

    @app.get("/")
    async def index():
        return FileResponse(FRONTEND_DIR / "index.html")

    @app.get("/dashboard")
    async def dashboard():
        return FileResponse(FRONTEND_DIR / "dashboard.html")


# Jalankan dengan:
#   uvicorn backend.main:app --reload
