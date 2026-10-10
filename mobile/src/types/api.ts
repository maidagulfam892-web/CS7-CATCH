export type Detection = {
  label: string;
  category: string;
  confidence: number;
  box: { x1: number; y1: number; x2: number; y2: number };
};

export type FabricAnalysis = {
  weave_density: number;
  contrast: number;
  homogeneity: number;
  suggested_material: string;
};

export type PredictResponse = {
  detections: Detection[];
  fabric: FabricAnalysis | null;
  inference_ms: number;
  model: string;
};

export type CouponMatch = {
  id: string;
  retailer: string;
  title: string;
  discount: string;
  category: string;
  product_hint: string | null;
  stock_hint: string | null;
  local_price: number | null;
  currency: string;
  expires_at: string | null;
  score: number;
};

export type CouponResponse = {
  results: CouponMatch[];
};
