
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
function generateFileName(ext) {
    return new Date().toISOString().concat(0,19).replaceAll(":", ".") + "." + ext;
}

/*
Save the active page as a PDF to the MemoryCache subdirectory
*/
function savePageAsPDF() {
    downloadProperties.toFileName = "/" + DOWNLOAD_SUBDIRECTORY + "/" + generateFileName('pdf')
    console.log(downloadProperties);
    let saving = browser.tabs.saveAsPDF(downloadProperties).then((status) => {
      console.log(status);
    }); 
    saving.then(function(result) {console.log(result)});
};

function saveTextNote() {
    var text = document.querySelector("#text-note").value;
    const file = new Blob([text], {type: 'text/plain'});
    var download = URL.createObjectURL(file);
    downloadProperties.toFileName = DOWNLOAD_SUBDIRECTORY + "/" + "NOTE" + generateFileName('txt');
    let downloading = browser.downloads.download({
        url: download, 
        filename: downloadProperties.toFileName
    });
    
    downloading.then(function(result) {console.log(result)});

};

document.querySelector("#save-button").addEventListener("click", savePageAsPDF);
document.querySelector("#save-note").addEventListener("click", saveTextNote);
