from fastapi import FastAPI
from typing import List
from llamafile_manager import get_llamafile_manager
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
import os
import sys

llamafiles_dir = os.environ.get('LLAMAFILES_DIR')
if not llamafiles_dir:
    raise ValueError("LLAMAFILES_DIR environment variable is not set")
manager = get_llamafile_manager(llamafiles_dir)

app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="Spin up a simple api server using Langchain's Runnable interfaces",
)

# Be sure to allow POST requests to the server by running the following command:
#

@app.get("/api/llamafile_manager/list_llamafiles", response_model=List[str])
async def list_llamafiles():
    llamafiles = manager.list_llamafiles()
    return llamafiles

@app.get("/api/llamafile_manager/has_llamafile/{name}", response_model=bool)
async def has_llamafile(name: str):
    return manager.has_llamafile(name)

@app.post("/api/llamafile_manager/download_llamafile")
async def download_llamafile(url: str, name: str):
    handle = manager.download_llamafile(url, name)
    return handle

@app.post("/api/llamafile_manager/download_progress")
async def download_progress(url: str, name: str):
    handle = next(h for h in manager.download_handles if h.url == url and h.filename == name)
    if handle is None:
        return 0
    return handle.progress()


class RunLlamafileRequest(BaseModel):
    name: str
    args: List[str]

@app.post("/api/llamafile_manager/run_llamafile")
async def run_llamafile(request: RunLlamafileRequest):
    # Check if it is already running
    print("Hello world! This is a test message.")
    print(manager.run_handles)
    if any(h for h in manager.run_handles if h.llamafile_name == request.name):
        return "already running"
    print(request.name, request.args)
    manager.run_llamafile(request.name, request.args)
    return "ok"

# Test the above method with curl:
# curl -XPOST -H "Content-Type: application/json" -d '{"name": "mistral-7b-instruct-v0.2.Q5_K_M.llamafile", "args": ["--host", "0.0.0.0", "--port", "8800"]}' http://localhost:8001/api/llamafile_manager/run_llamafile


class IsLlamafileRunningRequest(BaseModel):
    name: str

@app.post("/api/llamafile_manager/is_llamafile_running")
async def is_llamafile_running(request: IsLlamafileRunningRequest):
    return any(h.process is not None for h in manager.run_handles if h.filename == name)

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # The application is frozen by PyInstaller
    bundle_dir = sys._MEIPASS
else:
    # The application is running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

static_files_dir = os.path.join(bundle_dir, 'static')
app.mount("/", StaticFiles(directory=static_files_dir, html=True), name="static")

#static_files_dir = os.environ.get('STATIC_FILES_DIR', 'static')
#app.mount("/", StaticFiles(directory=static_files_dir, html=True), name="static")

# Test the above method with curl:
# curl -XPOST -H "Content-Type: application/json" -d '{"name": "mistral-7b-instruct-v0.2.Q5_K_M.llamafile"}' http://localhost:8001/api/llamafile_manager/is_llamafile_running
