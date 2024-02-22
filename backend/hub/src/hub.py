from llamafile_manager import LlamafileManager, update_tqdm
from llamafile_infos import llamafile_url_llava_v1_5_7b_q4, llamafile_name_llava_v1_5_7b_q4
from async_utils import start_async_loop, run
from tqdm import tqdm
import asyncio
import threading
import os
import subprocess
import requests
import time

async def main():
    loop = asyncio.new_event_loop()
    t = threading.Thread(target=start_async_loop, args=(loop,), daemon=True)
    t.start()

    llamafiles_dir = os.environ.get('LLAMAFILES_DIR')

    if not llamafiles_dir:
        raise ValueError("LLAMAFILES_DIR environment variable is not set")

    manager = LlamafileManager(llamafiles_dir)

    print("Llamafiles directory:", manager.llamafiles_dir)
    print("Available llamafiles:", manager.list_llamafiles())

    finish_event = None
    if manager.has_llamafile(llamafile_name_llava_v1_5_7b_q4):
        print("Llamafile", llamafile_name_llava_v1_5_7b_q4, "is available.")

    else:
        print("Downloading llamafile", llamafile_name_llava_v1_5_7b_q4)
        download_handle = manager.download_llamafile(llamafile_url_llava_v1_5_7b_q4, llamafile_name_llava_v1_5_7b_q4)
        pbar = tqdm(total=download_handle.content_length, unit="B", unit_scale=True)
        finish_event = run([download_handle.coroutine, update_tqdm(pbar, download_handle)], loop)

    if finish_event:
        finish_event.wait()
        pbar.close()
        print("Download finished.")
    else:
        print("Llamafile is already available.")

    print("Running", llamafile_name_llava_v1_5_7b_q4)
    args = ["--host", "0.0.0.0", "--port", "8800"]
    if os.environ.get('MEMORY_CACHE_ENABLE_GPU'):
        args.append('-ngl 999')
    run_handle = manager.run_llamafile(llamafile_name_llava_v1_5_7b_q4, args)
    print("Process started:", run_handle)

    while True:
        try:
            response = requests.get("http://localhost:8800")
            print(response)
            break
        except requests.exceptions.ConnectionError:
            print("Connection error, retrying in 1 second...")
            time.sleep(1)

    # Get user input in a loop. If user types "exit", break the loop.
    while True:
        user_input = input("\nType a prompt or type 'exit' to quit:\n  > ")
        if user_input.lower() == "exit":
            break
        print()
        # Send the prompt to the llamafile server
        print("Sending prompt to llamafile server:", user_input)
        print()

        # Prepare the a dictionary that will be sent to the server:
        data = {
            "stream": False,
            "n_predict": 400,
            "temperature": 0.7,
            "stop": ["</s>", "Llama:", "User:"],
            "repeat_last_n": 256,
            "repeat_penalty": 1.18,
            "top_k": 40,
            "top_p": 0.5,
            "tfs_z": 1,
            "typical_p": 1,
            "presence_penalty": 0,
            "frequency_penalty": 0,
            "mirostat": 0,
            "mirostat_tau": 5,
            "mirostat_eta": 0.1,
            "grammar": "",
            "n_probs": 0,
            "image_data": [],
            "cache_prompt": True,
            "slot_id": -1,
            "prompt": "This is a conversation between User and Llama, a friendly chatbot. Llama is helpful, kind, honest, good at writing, and never fails to answer any requests immediately and with precision.\n\nUser:" + user_input + "\nLlama:"
        }

        # Or, use requests to send the prompt to the server:
        post_req = requests.post("http://localhost:8800/completion", json=data)
        print(post_req.text)

    print("Stopping all llamafile servers...")
    manager.stop_all_llamafiles()
    print("All llamafile servers stopped.")

if __name__ == "__main__":
    asyncio.run(main())
