from pydantic import BaseModel, Field


class TryOnRequest(BaseModel):
    product_image_url: str | None = Field(default=None)
    page_url: str | None = None
    category: str | None = None
    silhouette: str | None = None


class OverlayAnchor(BaseModel):
    region: str
    scale: float
    opacity: float


class TryOnResponse(BaseModel):
    overlay_id: str
    category: str
    anchors: list[OverlayAnchor]
    coupon_hint: str | None = None
