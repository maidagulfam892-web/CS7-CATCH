import { env } from "../config/env";
import type { CouponResponse, PredictResponse } from "../types/api";

async function catchFetch(path: string, init: RequestInit = {}) {
  const response = await fetch(`${env.apiUrl}${path}`, {
    ...init,
    headers: {
      "X-API-Key": env.apiKey,
      ...(init.headers ?? {}),
    },
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `CATCH API ${response.status}`);
  }
  return response.json();
}

export async function predictImage(uri: string): Promise<PredictResponse> {
  const form = new FormData();

  if (uri.startsWith('data:') || uri.startsWith('blob:')) {
    const res = await fetch(uri);
    const blob = await res.blob();
    form.append("file", blob, "capture.jpg");
  } else {
    form.append("file", {
      uri,
      name: "capture.jpg",
      type: "image/jpeg",
    } as unknown as Blob);
  }

  form.append("include_fabric", "true");
  return catchFetch("/predict", { method: "POST", body: form });
}

export async function fetchCoupons(params: {
  lat?: number;
  lng?: number;
  category?: string;
  product_label?: string;
}): Promise<CouponResponse> {
  const query = new URLSearchParams();
  if (params.lat != null) query.set("lat", String(params.lat));
  if (params.lng != null) query.set("lng", String(params.lng));
  if (params.category) query.set("category", params.category);
  if (params.product_label) query.set("product_label", params.product_label);
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return catchFetch(`/coupons${suffix}`);
}
