const apiUrl = document.getElementById("apiUrl");
const apiKey = document.getElementById("apiKey");

chrome.storage.local.get(["apiUrl", "apiKey"]).then((stored) => {
  apiUrl.value = stored.apiUrl || "http://127.0.0.1:8000/api/v1";
  apiKey.value = stored.apiKey || "dev-api-key";
});

document.getElementById("save").addEventListener("click", async () => {
  await chrome.storage.local.set({
    apiUrl: apiUrl.value.trim(),
    apiKey: apiKey.value.trim(),
  });
  window.close();
});
