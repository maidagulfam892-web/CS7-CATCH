/**
 * Service worker proxies CATCH API calls so content scripts never hold the API key.
 */

const DEFAULT_API = "http://127.0.0.1:8000/api/v1";

async function getConfig() {
  const stored = await chrome.storage.local.get(["apiUrl", "apiKey"]);
  return {
    apiUrl: stored.apiUrl || DEFAULT_API,
    apiKey: stored.apiKey || "dev-api-key",
  };
}

async function catchRequest(path, options = {}) {
  const { apiUrl, apiKey } = await getConfig();
  const response = await fetch(`${apiUrl}${path}`, {
    ...options,
    headers: {
      "X-API-Key": apiKey,
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });
  if (!response.ok) {
    throw new Error(`CATCH API ${response.status}`);
  }
  return response.json();
}

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  (async () => {
    if (message.type === "CATCH_TRY_ON") {
      const overlay = await catchRequest("/try-on", {
        method: "POST",
        body: JSON.stringify(message.payload),
      });
      const coupons = await catchRequest(
        `/coupons?category=${encodeURIComponent(message.payload.category || "apparel")}`,
      );
      sendResponse({ ok: true, overlay, coupons });
      return;
    }
    if (message.type === "CATCH_COUPONS") {
      const params = new URLSearchParams(message.query || {});
      const coupons = await catchRequest(`/coupons?${params.toString()}`);
      sendResponse({ ok: true, coupons });
      return;
    }
    sendResponse({ ok: false, error: "Unknown message" });
  })().catch((error) => {
    sendResponse({ ok: false, error: error.message });
  });
  return true;
});
