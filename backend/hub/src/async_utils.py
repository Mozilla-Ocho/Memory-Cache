import threading
import asyncio

def start_async_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def wait_for(coroutines, finish_event):
    await asyncio.gather(*coroutines)
    finish_event.set()

def run(coroutines, loop):
    finish_event = threading.Event()
    asyncio.run_coroutine_threadsafe(wait_for(coroutines, finish_event), loop)
    return finish_event

def run_async(coroutines):
    finish_event = threading.Event()
    asyncio.run_coroutine_threadsafe(wait_for(coroutines, finish_event), get_my_loop())
    return finish_event

loop = None
def set_my_loop(l):
    global loop
    loop = l

def get_my_loop():
    global loop
    return loop
