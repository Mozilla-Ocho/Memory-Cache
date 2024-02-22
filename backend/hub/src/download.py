import aiohttp
import aiofiles
import asyncio

class DownloadHandle:
    def __init__(self):
        self.url = None
        self.filename = None
        self.content_length = 0
        self.written = 0
        self.coroutine = None

    def progress(self):
        return int(100 * self.written / self.content_length if self.content_length > 0 else 0)

    def __repr__(self):
        return f"DownloadHandle(url={self.url}, filename={self.filename}, content_length={self.content_length}, written={self.written})"

async def download(handle: DownloadHandle):
    async with aiohttp.ClientSession() as session:
        async with session.get(handle.url) as response:
            with open(handle.filename, 'wb') as f_handle:
                handle.content_length = int(response.headers.get('content-length', 0))
                handle.written = 0
                async with aiofiles.open(handle.filename, 'wb') as file:
                    async for data in response.content.iter_chunked(1024):
                        await file.write(data)
                        handle.written += len(data)

async def update_tqdm(pbar, handle: DownloadHandle):
    while handle.progress() < 100:
        # We don't know the total size until the download starts, so we update it here
        pbar.total = handle.content_length / 1024
        pbar.update(handle.written / 1024 - pbar.n)
        await asyncio.sleep(0.1)
