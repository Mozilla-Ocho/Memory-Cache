from llamafile_manager import get_llamafile_manager
from async_utils import start_async_loop, set_my_loop
import asyncio
import threading
import os
import uvicorn
import webbrowser
from fastapi_app import app
from gradio_app import iface

def run_api_server():
    uvicorn.run(app, host="localhost", port=8001)

def run_gradio_interface():
    iface.launch()

if __name__ == "__main__":

    llamafiles_dir = os.environ.get('LLAMAFILES_DIR')
    if not llamafiles_dir:
        raise ValueError("LLAMAFILES_DIR environment variable is not set")
    manager = get_llamafile_manager(llamafiles_dir)

    loop = asyncio.new_event_loop()
    set_my_loop(loop)
    t = threading.Thread(target=start_async_loop, args=(loop,), daemon=True)
    t.start()

    t2 = threading.Thread(target=run_api_server, daemon=True)
    t2.start()

    # t3 = threading.Thread(target=run_gradio_interface, daemon=True)
    # t3.start()

    webbrowser.open("http://localhost:8001/docs", new=0)
    #webbrowser.open("http://localhost:7860/", new=0)

    t.join()

    manager.stop_all_llamafiles()
