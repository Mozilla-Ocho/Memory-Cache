from llamafile_manager import update_tqdm, get_llamafile_manager
from llamafile_infos import llamafile_infos
from langchain_community.llms.llamafile import Llamafile
from typing import Generator
from typing import List
from async_utils import start_async_loop, run
from tqdm import tqdm
import asyncio
import threading
import os
import subprocess
import requests
import time
import webbrowser
import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from time import sleep
import webapp
from webapp import app

llamafiles_dir = os.environ.get('LLAMAFILES_DIR')
if not llamafiles_dir:
    raise ValueError("LLAMAFILES_DIR environment variable is not set")
manager = get_llamafile_manager(llamafiles_dir)

async def main():

    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_async_loop, args=(loop,), daemon=True)
    t.start()


    print("Llamafiles directory:", manager.llamafiles_dir)

    # Prompt the user to select a llamafile to download/run
    print("Select a llamafile:")
    for i, (name, url) in enumerate(llamafile_infos):
        # Show a number, the llamafile name, and whether the llamafile is already downloaded
        print(f"{i + 1}. {name} {'(available)' if manager.has_llamafile(name) else ''}")

    selection = input("Enter the number of the llamafile to download/run: ")
    selection = int(selection) - 1

    llamafile_name, llamafile_url = llamafile_infos[selection]

    finish_event = None
    if manager.has_llamafile(llamafile_name):
        print("Llamafile", llamafile_name, "is available.")

    else:
        print("Downloading llamafile", llamafile_name)
        download_handle = manager.download_llamafile(llamafile_url, llamafile_name)
        pbar = tqdm(total=download_handle.content_length, unit="B", unit_scale=True)
        finish_event = run([download_handle.coroutine, update_tqdm(pbar, download_handle)], loop)

    if finish_event:
        finish_event.wait()
        pbar.close()
        print("Download finished.")
    else:
        print("Llamafile is already available.")

    print("Running", llamafile_name)
    args = ["--host", "0.0.0.0", "--port", "8800"]
    if os.environ.get('MEMORY_CACHE_ENABLE_GPU'):
        args.append('-ngl 999')
    run_handle = manager.run_llamafile(llamafile_name, args)
    print("Process started:", run_handle)

    while True:
        try:
            response = requests.get("http://localhost:8800")
            print(response)
            break
        except requests.exceptions.ConnectionError:
            print("Connection error, retrying in 1 second...")
            time.sleep(1)

    #llm = Llamafile()

    # Get user input in a loop. If user types "exit", break the loop.
    while True:
        user_input = input("\nType a prompt or type 'exit' to quit:\n  > ")
        if user_input.lower() == "exit":
            break
        print()
        # Send the prompt to the llamafile server
        print("Sending prompt to llamafile server:", user_input)
        print()

        generator = llm.stream(user_input)
        assert isinstance(generator, Generator)
        for token in generator:
            assert isinstance(token, str)
            print(token, end="", flush=True)

    print("Stopping all llamafile servers...")
    manager.stop_all_llamafiles()
    print("All llamafile servers stopped.")



def run_async_main():
    asyncio.run(main())

def run_async_fastapi():

    llm = Llamafile(streaming=True)
    llm.base_url = "http://localhost:8800"

    add_routes(app,
        llm,
        path="/llm")

    # Need to allow POST requests to the server by running the following command:

    uvicorn.run(app, host="localhost", port=8001)

if __name__ == "__main__":
    t2 = threading.Thread(target=run_async_fastapi, daemon=True)
    t2.start()

    sleep(1)

    webbrowser.open("http://localhost:8001/", new=0)

    t = threading.Thread(target=run_async_main, daemon=True)
    t.start()

    t.join()
    t2.join()
