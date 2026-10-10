# CATCH

**Contextual Automated Tracking, Comparison and Hub for Coupons**

Hybrid edge–cloud retail platform: mobile capture, cloud vision + coupon matching, and a Chrome “Try-On Everywhere” extension.

## Repository layout

```
backend/     FastAPI inference, fabric analysis, coupon & retailer adapters
mobile/       Expo (React Native) edge client
extension/    Chrome Manifest V3 “Try-On Everywhere”
docs/         Architecture notes
```

## Quick start — API

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
copy ..\.env.example .env   # or cp
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Health: `GET http://localhost:8000/health`
- Docs: `http://localhost:8000/docs`

Place a YOLOv8 weights file at `backend/app/ml/weights/yolov8n.pt` (Ultralytics will download a default nano model on first run if missing, depending on environment).

## Quick start — mobile

```bash
cd mobile
npm install
npx expo start
```

Set `EXPO_PUBLIC_API_URL` and `EXPO_PUBLIC_API_KEY` in `mobile/.env`.

## Quick start — extension

1. Chrome → `chrome://extensions` → Developer mode
2. Load unpacked → `extension/`
3. In the popup, set API base URL and API key

## Design notes

- Vision and scraping stay **in the cloud**; the phone only preprocesses and uploads.
- Retail adapters should prefer official APIs and honor robots.txt / terms of service.
- Extension content scripts never embed the API key; the service worker proxies requests.
