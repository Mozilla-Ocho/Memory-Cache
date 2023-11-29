import { marked } from "./marked.esm.js";

const DOWNLOAD_SUBDIRECTORY = "MemoryCache";

/*
Generate a file name based on date and time
*/
function generateFileName(ext) {
  return (
    new Date().toISOString().concat(0, 19).replaceAll(":", ".") + "." + ext
  );
}

async function savePDF() {
  try {
    await browser.tabs.saveAsPDF({
      toFileName: `${DOWNLOAD_SUBDIRECTORY}/PAGE${generateFileName("pdf")}`,
      silentMode: true, // silentMode requires a custom build of Firefox
    });
  } catch (_e) {
    // Fallback to non-silent mode.
    await browser.tabs.saveAsPDF({
      // Omit the DOWNLOAD_SUBDIRECTORY prefix because saveAsPDF will not respect it.
      toFileName: `PAGE${generateFileName("pdf")}`,
    });
  }
}

// Send a message to the content script.
//
// We need code to run in the content script context for anything
// that accesses the DOM or needs to outlive the popup window.
function send(message) {
  return new Promise((resolve, _reject) => {
    browser.tabs.query({ active: true, currentWindow: true }, (tabs) => {
      resolve(browser.tabs.sendMessage(tabs[0].id, message));
    });
  });
}

async function saveHtml() {
  const text = await send({ action: "getPageText" });
  const filename = `${DOWNLOAD_SUBDIRECTORY}/PAGE${generateFileName("html")}`;
  const file = new File([text], filename, { type: "text/plain" });
  const url = URL.createObjectURL(file);
  browser.downloads.download({ url, filename, saveAs: false });
}

function saveNote() {
  const text = document.querySelector("#text-note").value;
  const filename = `${DOWNLOAD_SUBDIRECTORY}/NOTE${generateFileName("md")}`;
  const file = new File([text], filename, { type: "text/plain" });
  const url = URL.createObjectURL(file);
  browser.downloads.download({ url, filename, saveAs: false });

  document.querySelector("#text-note").value = "";
  browser.storage.local.set({ noteDraft: "" });
}

function debounce(func, delay) {
  let debounceTimer;
  return function () {
    const context = this;
    const args = arguments;
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => func.apply(context, args), delay);
  };
}

function saveNoteDraft() {
  const noteDraft = document.querySelector("#text-note").value;
  browser.storage.local.set({ noteDraft });
}

document.getElementById("save-pdf-button").addEventListener("click", savePDF);
document.getElementById("save-html-button").addEventListener("click", saveHtml);
document.getElementById("save-pdf-button").addEventListener("click", savePDF);
document.getElementById("save-note-button").addEventListener("click", saveNote);
document
  .getElementById("text-note")
  .addEventListener("input", debounce(saveNoteDraft, 250));

browser.storage.local.get("noteDraft").then((res) => {
  if (res.noteDraft) {
    document.querySelector("#text-note").value = res.noteDraft;
  }
});

function setTextView(showPreview) {
  var textArea = document.getElementById("text-note");
  var previewDiv = document.getElementById("preview-note");
  if (showPreview) {
    textArea.style.display = "none";
    previewDiv.style.display = "block";

    previewDiv.innerHTML = marked(textArea.value);
  } else {
    // Switch to editing mode
    previewDiv.style.display = "none";
    textArea.style.display = "block";
  }
}

document.getElementById("edit-button").addEventListener("click", () => {
  setTextView(false);
});

document.getElementById("preview-button").addEventListener("click", () => {
  setTextView(true);
});
