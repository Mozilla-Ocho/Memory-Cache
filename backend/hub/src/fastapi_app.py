from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
#from langchain_community.llms.llamafile import Llamafile
#from langserve import add_routes
import os
import sys
from api.thread_api import router as thread_router
from api.llamafile_api import router as llamafile_router

app = FastAPI(
    title="Memory Cache Hub",
    version="1.0",
    description="Manage llamafiles, document store, and vector database.",
)

app.include_router(thread_router, prefix="/api/thread")
app.include_router(llamafile_router, prefix="/api/llamafile")

#llm = Llamafile(streaming=True)
#llm.base_url = "http://localhost:8800"
#add_routes(app, llm, path="/llm")

if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    # The application is frozen by PyInstaller
    bundle_dir = sys._MEIPASS
else:
    # The application is running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

static_files_dir = os.path.join(bundle_dir, 'static')
app.mount("/static", StaticFiles(directory=static_files_dir, html=True), name="static")

