import os
import asyncio
import aiohttp
import aiofiles
#import certifi
import asyncio
import subprocess
import psutil

class DownloadHandle:
    def __init__(self):
        self.url = None
        self.filename = None
        self.llamafile_name = None
        self.content_length = 0
        self.written = 0
        self.coroutine = None

    def progress(self):
        return int(100 * self.written / self.content_length if self.content_length > 0 else 0)

    def __repr__(self):
        return f"DownloadHandle(url={self.url}, filename={self.filename}, content_length={self.content_length}, written={self.written})"

async def download(handle: DownloadHandle):
    # BUG On MacOS, https requests failed unless I disabled ssl checking.
    # TODO Fix ssl issue on MacOS
    #      This github issue may be related:
    #      https://github.com/aio-libs/aiohttp/issues/955
    #async with aiohttp.ClientSession() as session:
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
        async with session.get(handle.url) as response:
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

class RunHandle:
    def __init__(self):
        self.llamafile_name = None
        self.filename = None
        self.args = []
        self.process = None

    def __repr__(self):
        return f"RunHandle(filename={self.filename}, args={self.args}, process={self.process})"

_instance = None

def get_llamafile_manager(llamafiles_dir: str = None):
    global _instance
    if _instance is None:
        if llamafiles_dir is None:
            raise ValueError("Must specify llamafiles_dir when creating the LlamafileManager instance")
        _instance = LlamafileManager(llamafiles_dir)
    return _instance

class LlamafileManager:
    def __init__(self, llamafiles_dir: str):
        self.llamafiles_dir = llamafiles_dir
        self.download_handles = []
        self.run_handles = []

    def list_llamafiles(self):
        return [f for f in os.listdir(self.llamafiles_dir) if f.endswith('.llamafile')]

    def has_llamafile(self, name):
        return name in self.list_llamafiles()

    def download_llamafile(self, url, name):
        handle = DownloadHandle()
        self.download_handles.append(handle)
        handle.url = url
        handle.llamafile_name = name
        handle.filename = os.path.join(self.llamafiles_dir, name)
        handle.coroutine = download(handle)
        return handle

    def run_llamafile(self, name: str, args: list):
        if not self.has_llamafile(name):
            raise ValueError(f"llamafile {name} is not available")
        handle = RunHandle()
        self.run_handles.append(handle)
        handle.llamafile_name = name
        handle.filename = os.path.join(self.llamafiles_dir, name)
        # Print the file path, and check if the file exists
        print(handle.filename)
        if not os.path.isfile(handle.filename):
            raise FileNotFoundError(f"{name} not found in {self.llamafiles_dir}")
        if os.name == 'posix' or os.name == 'darwin':
            if not os.access(handle.filename, os.X_OK):
                os.chmod(handle.filename, 0o755)
        handle.args = args
        cmd = f"{handle.filename} {' '.join(args)}"
        handle.process = subprocess.Popen(["sh", "-c", cmd])

        return handle


    def stop_llamafile(self, handle: RunHandle):
        print(f"Stopping process {handle.process.pid}")
        if handle.process.poll() is None:
            try:
                parent = psutil.Process(handle.process.pid)
                children = parent.children(recursive=True)  # Get all child processes
                for child in children:
                    print(f"Terminating child process {child.pid}, {child.name()}")
                    child.terminate()  # Terminate each child
                gone, still_alive = psutil.wait_procs(children, timeout=3, callback=None)
                for p in still_alive:
                    p.kill()  # Force kill if still alive after timeout
                print(f"Terminating parent process {parent.pid}, {parent.name()}")
                handle.process.terminate()  # Terminate the parent process
                handle.process.wait()  # Wait for the parent process to terminate
            except psutil.NoSuchProcess:
                print(f"Process {handle.process.pid} does not exist anymore.")
            self.run_handles.remove(handle)
        else:
            print(f"Process {handle.process.pid} is not running")

    def stop_all_llamafiles(self):
        for handle in self.run_handles:
            self.stop_llamafile(handle)
        self.run_handles.clear()
