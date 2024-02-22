import os
import asyncio
from download import download, DownloadHandle

async def report_progress(my_handle):
    while my_handle.progress() < 100:
        print("Download status:", my_handle.progress())
        await asyncio.sleep(1)


class LlamafileManager:
    def __init__(self, llamafiles_dir: str):
        self.llamafiles_dir = llamafiles_dir
        self.download_handles = []

    def list_llamafiles(self):
        return [f for f in os.listdir(self.llamafiles_dir) if f.endswith('.llamafile')]

    def has_llamafile(self, name):
        return name in self.list_llamafiles()

    def download_llamafile(self, url, name):
        """Returns a DownloadHandle and a coroutine that must be awaited."""
        handle = DownloadHandle()
        handle.url = url
        handle.filename = os.path.join(self.llamafiles_dir, name)
        handle.coroutine = download(handle)
        return handle
