"""Hyper-local price/stock adapters.

Prefer official retailer APIs. HTTP fetches must honor robots.txt and Terms of Service.
This module ships a mock catalog plus a pluggable adapter interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone

import httpx

from app.core.config import get_settings


@dataclass
class RetailOffer:
    retailer: str
    title: str
    category: str
    product_hint: str
    local_price: float
    currency: str
    stock_hint: str
    discount: str
    coupon_id: str
    expires_at: str | None


MOCK_OFFERS: list[RetailOffer] = [
    RetailOffer(
        retailer="Harbor Market",
        title="20% off denim jackets",
        category="apparel",
        product_hint="jacket",
        local_price=59.99,
        currency="USD",
        stock_hint="in_stock",
        discount="20%",
        coupon_id="hm-denim-20",
        expires_at="2026-12-31",
    ),
    RetailOffer(
        retailer="City Threads",
        title="$10 off accessories over $40",
        category="accessory",
        product_hint="handbag",
        local_price=42.00,
        currency="USD",
        stock_hint="low_stock",
        discount="$10",
        coupon_id="ct-acc-10",
        expires_at="2026-11-15",
    ),
    RetailOffer(
        retailer="Northside Co-op",
        title="Student 15% on everyday apparel",
        category="apparel",
        product_hint="shirt",
        local_price=24.50,
        currency="USD",
        stock_hint="in_stock",
        discount="15%",
        coupon_id="nc-student-15",
        expires_at=None,
    ),
]


async def fetch_live_catalog(lat: float | None, lng: float | None) -> list[RetailOffer]:
    """Optional outbound fetch. Defaults to the mock catalog if no feed is configured."""
    settings = get_settings()
    feed_url = None  # wire a consented feed URL here
    if not feed_url:
        return MOCK_OFFERS

    headers = {"User-Agent": settings.scrape_user_agent}
    timeout = settings.scrape_timeout_seconds
    try:
        async with httpx.AsyncClient(timeout=timeout, headers=headers) as client:
            response = await client.get(feed_url, params={"lat": lat, "lng": lng})
            response.raise_for_status()
            payload = response.json()
    except httpx.HTTPError:
        return MOCK_OFFERS

    offers: list[RetailOffer] = []
    for row in payload.get("offers", []):
        offers.append(
            RetailOffer(
                retailer=row.get("retailer", "unknown"),
                title=row.get("title", ""),
                category=row.get("category", "general"),
                product_hint=row.get("product_hint", ""),
                local_price=float(row.get("local_price", 0)),
                currency=row.get("currency", "USD"),
                stock_hint=row.get("stock_hint", "unknown"),
                discount=row.get("discount", ""),
                coupon_id=row.get("coupon_id", ""),
                expires_at=row.get("expires_at"),
            )
        )
    return offers or MOCK_OFFERS


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
