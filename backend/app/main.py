from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import __version__
from app.api.routes import api_router
from app.core.config import get_settings

settings = get_settings()

app = FastAPI(
    title="CATCH Cloud Platform API",
    description="""
    ### 🚀 Contextual Automated Tailoring & Coupon Hub (CATCH)
    
    Yeh CATCH project ka core cloud backend engine hai, jo edge-client aur AI modules ko connect karta hai.
    
    * **Inference & Detection:** Smart clothing aur object tracking.
    * **Fabric Analysis:** Advanced texture aur material recognition.
    * **Smart Coupons:** Dynamic pricing aur adaptive discount engine.
    * **Virtual Try-On:** Real-time overlay rendering pipeline.
    """,
    version=__version__,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.api_prefix)

@app.get("/")
def root():
    return {"status": "ok", "message": "CATCH Cloud API is running"}

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "catch-api", "version": __version__}