
const DOWNLOAD_SUBDIRECTORY = "MemoryCache";

let downloadProperties = {
    toFileName: "", 
    silentMode: true
}

function onError(error) {
    console.log(`Error: ${error}`);
}

/* 
Generate a file name based on date and time
*/
function generateFileName() {
    return new Date().toISOString().concat(0,19).replaceAll(":", ".") + ".pdf";
}

/*
Save the active page as a PDF to the MemoryCache subdirectory
*/
function savePageAsPDF() {
    downloadProperties.toFileName = "/" + DOWNLOAD_SUBDIRECTORY + "/" + generateFileName()
    console.log(downloadProperties);
    let saving = browser.tabs.saveAsPDF(downloadProperties).then((status) => {
      console.log(status);
    }); 
    saving.then(function(result) {console.log(result)});
};

document.querySelector("#save-button").addEventListener("click", savePageAsPDF);
window.addEventListener("load", getCurrentPageDetails);
