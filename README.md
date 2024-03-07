# Memory Cache 

Memory Cache is a project that allows you to save a webpage while you're browsing in Firefox as a PDF, and save it to a synchronized folder that can be used in conjunction with privateGPT to augment a local language model.

| ⚠️: This setup uses the primordial version of privateGPT. I'm working from a fork that can be found [here](https://github.com/misslivirose/privateGPT).  |
| ---------------------------------------------------------------------------------------------------------------------- |

## Prerequisites 
1. Set up [privateGPT](https://github.com/imartinez/privateGPT) - either using the primordial checkpoint, or from my fork.
2. Create a symlink between a subdirectory in your default Downloads folder called 'MemoryCache' and a 'MemoryCache' directory created inside of /PrivateGPT/source_documents/MemoryCache 
3. Apply patch to Firefox to add the `printerSettings.silentMode` property to the Tabs API. [See wiki page for instructions](https://github.com/Mozilla-Ocho/Memory-Cache/wiki/Modifying-Firefox-to-Save-PDF-files-automagically-to-MemoryCache)
4. Copy /scripts/run_ingest.sh into your privateGPT directory and run it to start `inotifywait` watching your downloads directory for new content

## Setting up the Extension
1. Clone the Memory-Cache GitHub repository to your local machine 
2. In Firefox, navigate to `about:debugging` and click on 'This Firefox'
3. Click 'Load Temporary Add-on" and open the `extension/manifest.json` file in the MemoryCacheExt directory

## Using the Extension
1. Under the 'Extensions' menu, add the Memory Cache extension to the toolbar
2. When you want to save a page to your Memory Cache, click the icon and select the 'Save' button. This will save the file silently as a PDF if you are using a Firefox build with the `printerSettings.silentMode` property addition.
