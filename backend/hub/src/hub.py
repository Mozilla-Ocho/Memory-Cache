from llamafile_manager import LlamafileManager
from llamafile_infos import llamafile_url_llava_v1_5_7b_q4, llamafile_name_llava_v1_5_7b_q4
from async_utils import start_async_loop, run
from download import update_tqdm
from tqdm import tqdm
import asyncio
import threading
import os

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
        print("Downloading", llamafile_name_llava_v1_5_7b_q4)
        download_handle = manager.download_llamafile(llamafile_url_llava_v1_5_7b_q4, llamafile_name_llava_v1_5_7b_q4)
        pbar = tqdm(total=download_handle.content_length, unit="KB", unit_scale=True)
        finish_event = run([download_handle.coroutine, update_tqdm(pbar, download_handle)], loop)

    if finish_event:
        finish_event.wait()
        if pbar:
            pbar.close()
        print("Download finished.")

    exit()

if __name__ == "__main__":
    asyncio.run(main())
