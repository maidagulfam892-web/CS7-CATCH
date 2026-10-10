from fastapi import APIRouter, Depends, Query

from app.core.security import require_api_key
from app.schemas.coupon import CouponQuery, CouponResponse
from app.services.coupons import match_coupons

router = APIRouter()


@router.get("/coupons", response_model=CouponResponse)
async def list_coupons(
    lat: float | None = Query(default=None),
    lng: float | None = Query(default=None),
    category: str | None = Query(default=None),
    product_label: str | None = Query(default=None),
    limit: int = Query(default=10, ge=1, le=50),
    _: str = Depends(require_api_key),
) -> CouponResponse:
    query = CouponQuery(
        lat=lat,
        lng=lng,
        category=category,
        product_label=product_label,
        limit=limit,
    )
    return await match_coupons(query)
