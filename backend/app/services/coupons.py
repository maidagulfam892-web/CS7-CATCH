from __future__ import annotations

from app.schemas.coupon import CouponMatch, CouponQuery, CouponResponse
from app.services.retailers import RetailOffer, fetch_live_catalog


def _score(offer: RetailOffer, query: CouponQuery) -> float:
    score = 0.4
    if query.category and query.category.lower() == offer.category.lower():
        score += 0.35
    if query.product_label:
        hint = (offer.product_hint + " " + offer.title).lower()
        if query.product_label.lower() in hint:
            score += 0.25
    if query.lat is not None:
        score += 0.05
    return round(min(score, 1.0), 3)


async def match_coupons(query: CouponQuery) -> CouponResponse:
    catalog = await fetch_live_catalog(query.lat, query.lng)
    ranked: list[tuple[float, RetailOffer]] = []
    for offer in catalog:
        if query.category and query.category.lower() != offer.category.lower():
            continue
        ranked.append((_score(offer, query), offer))

    ranked.sort(key=lambda pair: pair[0], reverse=True)
    results = [
        CouponMatch(
            id=offer.coupon_id,
            retailer=offer.retailer,
            title=offer.title,
            discount=offer.discount,
            category=offer.category,
            product_hint=offer.product_hint,
            stock_hint=offer.stock_hint,
            local_price=offer.local_price,
            currency=offer.currency,
            expires_at=offer.expires_at,
            score=score,
        )
        for score, offer in ranked[: query.limit]
    ]
    return CouponResponse(query=query, results=results)
