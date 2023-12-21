const DOWNLOAD_SUBDIRECTORY = "MemoryCache";

/*
Generate a file name based on date and time
*/

function getTabTitle() {}

async function generateFileName(ext) {
  var subfileName =
    new Date().toISOString().concat(0, 19).replaceAll(":", ".") + "." + ext;

  return browser.tabs
    .query({ active: true })
    .then((tabs) => {
      if (tabs && tabs[0] && tabs[0].title) {
        console.log(tabs[0].title);
        return tabs[0].title.replaceAll(" ", "-") + "-" + subfileName;
      } else {
        return subfileName;
      }
    })
    .catch((error) => {
      reject(`Error querying tabs: ${error}`);
    });
}

async function savePDF() {
  try {
    var fileName = await generateFileName("pdf");
    await browser.tabs.saveAsPDF({
      toFileName: `/${DOWNLOAD_SUBDIRECTORY}/PAGE-${fileName}`,
      silentMode: true, // silentMode requires a custom build of Firefox
    });
  } catch (_e) {
    // Fallback to non-silent mode.
    await browser.tabs.saveAsPDF({
      // Omit the DOWNLOAD_SUBDIRECTORY prefix because saveAsPDF will not respect it.
      toFileName: `PAGE-${generateFileName("pdf")}`,
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
  var fileName = await generateFileName("html");
  const text = await send({ action: "getPageText" });
  fileName = `${DOWNLOAD_SUBDIRECTORY}/PAGE-${fileName}`;
  const file = new File([text], fileName, { type: "text/plain" });
  const url = URL.createObjectURL(file);
  browser.downloads.download({ url, filename: fileName, saveAs: false });
}

async function saveNote() {
  var fileName = await generateFileName("txt");
  const text = document.querySelector("#text-note").value;
  fileName = `${DOWNLOAD_SUBDIRECTORY}/NOTE-${fileName}`;
  const file = new File([text], fileName, { type: "text/plain" });
  const url = URL.createObjectURL(file);
  browser.downloads.download({ url, filename: fileName, saveAs: false });

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
