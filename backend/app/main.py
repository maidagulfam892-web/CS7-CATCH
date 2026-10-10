from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="CATCH Cloud API",
    description="Inference, fabric analysis, coupons, and try-on overlays.",
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origin_list,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type", "X-API-Key"],
)

app.include_router(api_router, prefix=settings.api_prefix)

@app.get("/")
def root():
    return {"status": "ok", "message": "CATCH Cloud API is running"}

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "catch-api", "version": __version__}
