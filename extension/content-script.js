function getPageText() {
  const head = document.head.innerHTML;
  const body = document.body.innerText;
  return `<!DOCTYPE html>\n<head>\n${head}\n</head>\n<body>\n${body}\n</body>\n</html>`;
}

browser.runtime.onMessage.addListener((message, _sender) => {
  console.log("[MemoryCache Extension] Received message:", message);
  if (message.action === "getPageText") {
    return Promise.resolve(getPageText());
  }
});
