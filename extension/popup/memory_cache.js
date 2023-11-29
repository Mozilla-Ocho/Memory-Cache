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

function saveNote() {
  const text = document.querySelector("#text-note").value;
  const filename = `${DOWNLOAD_SUBDIRECTORY}/NOTE${generateFileName("txt")}`;
  const file = new File([text], filename, { type: "text/plain" });
  const url = URL.createObjectURL(file);
  browser.downloads.download({ url, filename, saveAs: false });
}

document.getElementById("save-pdf-button").addEventListener("click", savePDF);
document.getElementById("save-note-button").addEventListener("click", saveNote);
