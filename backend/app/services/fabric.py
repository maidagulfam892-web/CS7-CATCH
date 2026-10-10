"""OpenCV-based fabric texture metrics (GLCM-style proxies)."""

from __future__ import annotations

import cv2
import numpy as np

from app.schemas.predict import FabricAnalysis


def analyze_fabric(rgb: np.ndarray) -> FabricAnalysis:
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA)

    contrast = float(gray.std())
    laplacian = cv2.Laplacian(gray, cv2.CV_64F)
    weave_density = float(np.mean(np.abs(laplacian)))

    hist = cv2.calcHist([gray], [0], None, [32], [0, 256])
    hist = hist / (hist.sum() + 1e-8)
    homogeneity = float(np.sum(hist**2))

    if weave_density > 18 and contrast > 35:
        material = "denim-or-twill"
    elif weave_density < 8 and homogeneity > 0.08:
        material = "knit-or-jersey"
    elif contrast < 20:
        material = "smooth-synthetic"
    else:
        material = "woven-cotton-blend"

    return FabricAnalysis(
        weave_density=round(weave_density, 3),
        contrast=round(contrast, 3),
        homogeneity=round(homogeneity, 4),
        suggested_material=material,
    )
