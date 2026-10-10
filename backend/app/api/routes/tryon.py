from fastapi import APIRouter, Depends

from app.core.security import require_api_key
from app.schemas.tryon import TryOnRequest, TryOnResponse
from app.services.tryon import build_tryon

router = APIRouter()


@router.post("/try-on", response_model=TryOnResponse)
async def try_on(
    payload: TryOnRequest,
    _: str = Depends(require_api_key),
) -> TryOnResponse:
    return build_tryon(payload)
