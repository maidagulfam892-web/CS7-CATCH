from pydantic import BaseModel, Field


class CouponQuery(BaseModel):
    lat: float | None = Field(default=None, ge=-90, le=90)
    lng: float | None = Field(default=None, ge=-180, le=180)
    category: str | None = None
    product_label: str | None = None
    limit: int = Field(default=10, ge=1, le=50)


class CouponMatch(BaseModel):
    id: str
    retailer: str
    title: str
    discount: str
    category: str
    product_hint: str | None = None
    stock_hint: str | None = None
    local_price: float | None = None
    currency: str = "USD"
    expires_at: str | None = None
    score: float


class CouponResponse(BaseModel):
    query: CouponQuery
    results: list[CouponMatch]
