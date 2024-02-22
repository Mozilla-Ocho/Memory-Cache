Write a python module called `llamafile_manager.py` that meets the following requirements:
- Allows the creation of a struct or class called `LlamafileManager` that holds on to configuration, download, and process information
- Defines a function `list_llamafiles` that lists the files matching *.llamafile in the `llamafiles_dir`
- Defines a function `has_llamafile` that checks whether a given llamafile exists in the `llamafiles_dir` 
- Defines a function `download_llamafile(url, name)` that will download a llamafile into the `llamafiles_dir`
- Defines a function `run_llamafile` that will run the given llamafile (by name) as a subprocess
- Defines a function `stop_llamafile` that will stop the subprocess (and update the associated `llamafile_run_handle`)
- Define a function `check_download_status(llamafile_download_handle)` that returns a number between 0 and 100 indicating that status of an ongoing (or complete) download.

The `download_llamafile` function should:
- Kick off the download asynchronously and return a handle that can be used to check the status of a download.
- Check whether a download for the given url has already been initiated. If it has, return the existing download handle.

The `run_llamafile` function should:
- Return a llamafile_run_handle that can be used to check whether the subprocess is still running, or passed to `stop_llamafile` to stop it.
- If the specified llamafile is already running, return the existing `llamafile_run_handle`.
- Accept the name of a llamafile, an `http_host` (defaults to "0.0.0.0"), and an `http_port` (defaults to `8800`).

The `LlamafileManager` should hold onto information such as:
- `llamafiles_dir` (passed into its constructor)
- `llamafile_run_handle`s
- `llamafile_download_handle`s
