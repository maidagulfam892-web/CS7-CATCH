# CATCH Architecture

CATCH (Contextual Automated Tracking, Comparison and Hub for Coupons) is a hybrid **edge–cloud** retail assistant.

```
┌─────────────────────────┐     HTTPS + FCM      ┌──────────────────────────────────┐
│  Edge: Expo / RN app    │◄────────────────────►│  Cloud: FastAPI                  │
│  camera, preprocess, UI │                      │  YOLOv8, OpenCV fabric, coupons  │
└─────────────────────────┘                      │  retailer adapters / scrape      │
                                                 └──────────────▲───────────────────┘
┌─────────────────────────┐     HTTPS + API key                 │
│  Chrome MV3 extension   │◄────────────────────────────────────┘
│  page scan, AR overlay, │
│  coupon match, try-on   │
└─────────────────────────┘
```

## Layers

| Layer | Stack | Responsibility |
| --- | --- | --- |
| Edge | React Native, Expo, FCM | Capture, light preprocess, notifications, coupon UX |
| Cloud | FastAPI, Ultralytics YOLOv8, OpenCV | Detection, fabric analysis, pricing, matching |
| Browser | Manifest V3 | Scan product pages, overlay try-on UI, call `/predict` and `/coupons` |

## API contract (v1)

- `POST /api/v1/predict` — image → detections + optional fabric metrics
- `GET /api/v1/coupons` — geo + category → ranked offers
- `POST /api/v1/try-on` — product URL/image + silhouette hints → overlay payload

Clients send `X-API-Key`. CORS is restricted to the Expo web origin and the extension id.
