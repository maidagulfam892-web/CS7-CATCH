from __future__ import annotations

import hashlib

from app.schemas.tryon import OverlayAnchor, TryOnRequest, TryOnResponse

CATEGORY_ANCHORS = {
    "apparel": [
        OverlayAnchor(region="torso", scale=1.0, opacity=0.85),
        OverlayAnchor(region="shoulders", scale=1.05, opacity=0.7),
    ],
    "accessory": [
        OverlayAnchor(region="hand", scale=0.6, opacity=0.9),
    ],
    "body": [
        OverlayAnchor(region="full", scale=1.0, opacity=0.5),
    ],
}


def build_tryon(payload: TryOnRequest) -> TryOnResponse:
    category = (payload.category or "apparel").lower()
    seed = f"{payload.page_url}|{payload.product_image_url}|{category}"
    overlay_id = hashlib.sha256(seed.encode()).hexdigest()[:12]
    anchors = CATEGORY_ANCHORS.get(category, CATEGORY_ANCHORS["apparel"])
    return TryOnResponse(
        overlay_id=overlay_id,
        category=category,
        anchors=anchors,
        coupon_hint="Match coupons with GET /api/v1/coupons after detection.",
    )
