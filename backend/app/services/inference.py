from __future__ import annotations

import time
from functools import lru_cache
from pathlib import Path

import numpy as np
from PIL import Image

from app.core.config import get_settings
from app.schemas.predict import BoundingBox, Detection, PredictResponse
from app.services.fabric import analyze_fabric

CATEGORY_MAP = {
    "person": "body",
    "handbag": "accessory",
    "backpack": "accessory",
    "umbrella": "accessory",
    "tie": "apparel",
    "suitcase": "accessory",
}


@lru_cache(maxsize=1)
def _load_model():
    settings = get_settings()
    from ultralytics import YOLO

    weights = Path(settings.yolo_weights)
    model_src = str(weights) if weights.exists() else "yolov8n.pt"
    return YOLO(model_src)


def _category_for(label: str) -> str:
    return CATEGORY_MAP.get(label.lower(), "general")


def run_predict(image: Image.Image, include_fabric: bool = True) -> PredictResponse:
    settings = get_settings()
    started = time.perf_counter()
    rgb = np.array(image.convert("RGB"))

    try:
        model = _load_model()
        results = model.predict(
            source=rgb,
            device=settings.yolo_device,
            verbose=False,
        )
        detections: list[Detection] = []
        for result in results:
            names = result.names
            if result.boxes is None:
                continue
            for box in result.boxes:
                xyxy = box.xyxy[0].tolist()
                cls_id = int(box.cls[0])
                label = str(names.get(cls_id, cls_id))
                detections.append(
                    Detection(
                        label=label,
                        category=_category_for(label),
                        confidence=float(box.conf[0]),
                        box=BoundingBox(
                            x1=xyxy[0], y1=xyxy[1], x2=xyxy[2], y2=xyxy[3]
                        ),
                    )
                )
        model_name = Path(getattr(model, "ckpt_path", "yolov8n.pt")).name
    except Exception:
        detections = []
        model_name = "fallback-none"

    fabric = None
    if include_fabric:
        fabric = analyze_fabric(rgb)

    elapsed_ms = (time.perf_counter() - started) * 1000
    return PredictResponse(
        detections=detections,
        fabric=fabric,
        inference_ms=round(elapsed_ms, 2),
        model=model_name,
    )
