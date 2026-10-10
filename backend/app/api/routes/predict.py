from io import BytesIO

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError

from app.core.config import get_settings
from app.core.security import require_api_key
from app.schemas.predict import PredictResponse
from app.services.inference import run_predict

router = APIRouter()


@router.post("/predict", response_model=PredictResponse)
async def predict(
    file: UploadFile = File(..., description="RGB still from the edge camera"),
    include_fabric: bool = Form(default=True),
    _: str = Depends(require_api_key),
) -> PredictResponse:
    settings = get_settings()
    raw = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(raw) > max_bytes:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"Image exceeds {settings.max_upload_mb} MB",
        )
    try:
        image = Image.open(BytesIO(raw))
        image.load()
    except (UnidentifiedImageError, OSError) as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unreadable image payload",
        ) from exc

    return run_predict(image, include_fabric=include_fabric)
