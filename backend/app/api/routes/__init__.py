from fastapi import APIRouter

from app.api.routes import coupons, predict, tryon

api_router = APIRouter()
api_router.include_router(predict.router, tags=["inference"])
api_router.include_router(coupons.router, tags=["coupons"])
api_router.include_router(tryon.router, tags=["try-on"])
