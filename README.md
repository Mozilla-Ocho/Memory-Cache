![Incomplete Readme(2)](https://github.com/misslivirose/MemoryCacheExt/assets/4313320/adc46592-04ea-4d6d-b893-66477e24d636)

# Memory Cache - Firefox Extension

Memory Cache is a project that allows you to save a webpage while you're browsing in Firefox as a PDF, and save it to a synchronized folder that can be used in conjunction with privateGPT to augment a local language model.

## Prerequisites 
1. Set up [privateGPT](https://github.com/imartinez/privateGPT) 
2. Create a symlink between a subdirectory in your default Downloads folder called 'MemoryCache' and a 'MemoryCache' directory created inside of /PrivateGPT/source_documents/MemoryCache 
3. Apply patch to Firefox to add the `printerSettings.silentMode` property to the Tabs API. 

## Setting up the Extension
1. Clone the MemoryCacheExt GitHub repository to your local machine 
2. In Firefox, navigate to `about:debugging` and click on 'This Firefox'
3. Click 'Load Temporary Add-on" and open the `manifest.json` file in the MemoryCacheExt directory

## Using the Extension
1. Under the 'Extensions' menu, add the Memory Cache extension to the toolbar
2. When you want to save a page to your Memory Cache, click the icon and select the 'Save' button. This will save the file silently as a PDF if you are using a Firefox build with the `printerSettings.silentMode`  property addition. 

## Known Issues
* I need to document the process I used to modify Firefox

* The `ingest.py` script in privateGPT needs to be manually run when new files are added. In the future, adding a worker to automatically run the ingestion script after adding new files on a regular update cadence will reduce the manual steps. 
