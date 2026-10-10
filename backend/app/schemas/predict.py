from pydantic import BaseModel, Field


class BoundingBox(BaseModel):
    x1: float
    y1: float
    x2: float
    y2: float


class Detection(BaseModel):
    label: str
    category: str
    confidence: float = Field(ge=0, le=1)
    box: BoundingBox


class FabricAnalysis(BaseModel):
    weave_density: float
    contrast: float
    homogeneity: float
    suggested_material: str


class PredictResponse(BaseModel):
    detections: list[Detection]
    fabric: FabricAnalysis | None = None
    inference_ms: float
    model: str
