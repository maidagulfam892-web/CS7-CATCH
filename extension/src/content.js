/**
 * CATCH content script: finds product imagery, requests try-on overlays,
 * and injects a coupon rail without exposing backend credentials.
 */

const PRODUCT_IMAGE_SELECTORS = [
  'meta[property="og:image"]',
  'img[itemprop="image"]',
  'img[class*="product"]',
  'img[id*="product"]',
  'img[alt*="product" i]',
];

function findProductImage() {
  for (const selector of PRODUCT_IMAGE_SELECTORS) {
    const node = document.querySelector(selector);
    if (!node) continue;
    if (node.tagName === "META") {
      return node.getAttribute("content");
    }
    if (node instanceof HTMLImageElement && node.src) {
      return node.src;
    }
  }
  const largest = [...document.images]
    .filter((img) => img.naturalWidth >= 200 && img.naturalHeight >= 200)
    .sort((a, b) => b.naturalWidth * b.naturalHeight - a.naturalWidth * a.naturalHeight)[0];
  return largest?.src ?? null;
}

function inferCategory() {
  const text = `${document.title} ${document.body?.innerText?.slice(0, 2000) || ""}`.toLowerCase();
  if (/bag|handbag|backpack|wallet/.test(text)) return "accessory";
  if (/jacket|shirt|dress|jeans|apparel|clothing/.test(text)) return "apparel";
  return "apparel";
}

function ensureHost() {
  let host = document.getElementById("catch-tryon-host");
  if (host) return host;
  host = document.createElement("aside");
  host.id = "catch-tryon-host";
  host.setAttribute("data-catch", "overlay");
  document.documentElement.appendChild(host);
  return host;
}

function renderOverlay(payload) {
  const host = ensureHost();
  const coupons = payload.coupons?.results ?? [];
  const couponHtml = coupons
    .slice(0, 3)
    .map(
      (c) =>
        `<li><strong>${escapeHtml(c.discount)}</strong> ${escapeHtml(c.title)} · ${escapeHtml(c.retailer)}</li>`,
    )
    .join("");

  host.innerHTML = `
    <div class="catch-panel">
      <header>
        <span class="catch-mark">CATCH</span>
        <span class="catch-sub">Try-On Everywhere</span>
      </header>
      <p>Overlay <code>${escapeHtml(payload.overlay.overlay_id)}</code> · ${escapeHtml(payload.overlay.category)}</p>
      <ul class="catch-anchors">
        ${payload.overlay.anchors
          .map((a) => `<li>${escapeHtml(a.region)} ×${a.scale}</li>`)
          .join("")}
      </ul>
      <h3>Matched coupons</h3>
      <ul class="catch-coupons">${couponHtml || "<li>No local matches yet</li>"}</ul>
    </div>
  `;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;");
}

function scanPage() {
  const productImage = findProductImage();
  const category = inferCategory();
  chrome.runtime.sendMessage(
    {
      type: "CATCH_TRY_ON",
      payload: {
        page_url: location.href,
        product_image_url: productImage,
        category,
        silhouette: "auto",
      },
    },
    (response) => {
      if (chrome.runtime.lastError || !response?.ok) {
        return;
      }
      renderOverlay(response);
    },
  );
}

if (document.readyState === "complete") {
  scanPage();
} else {
  window.addEventListener("load", scanPage, { once: true });
}
