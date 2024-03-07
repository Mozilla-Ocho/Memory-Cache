import gradio as gr
import requests
from time import sleep

# Define functions that will interact with the FastAPI endpoints
def list_llamafiles():
    # If the request fails, it throws an error. We do not want the app to crash, so we catch the error and return an empty string.
    try:
        response = requests.get("http://localhost:8001/api/llamafile_manager/list_llamafiles")
        if response.status_code == 200:
            return "\n".join(response.json())
        return ""
    except:
        return ""

def has_llamafile(name):
    response = requests.get(f"http://localhost:8001/api/llamafile_manager/has_llamafile/{name}")
    if response.status_code == 200:
        return response.json()
    return "Error checking llamafile."

def download_llamafile(url, name):
    response = requests.post("http://localhost:8001/api/llamafile_manager/download_llamafile", json={"url": url, "name": name})
    if response.status_code == 200:
        return "Download initiated."
    return "Failed to initiate download."

def download_progress(url, name):
    response = requests.post("http://localhost:8001/api/llamafile_manager/download_progress", json={"url": url, "name": name})
    if response.status_code == 200:
        return response.json()
    return "Failed to get download progress."

def run_llamafile(name, args):
    response = requests.post("http://localhost:8001/api/llamafile_manager/run_llamafile", json={"name": name, "args": args.split()})
    if response.status_code == 200:
        return response.text
    return "Failed to run llamafile."

num = 0
def increment():
    global num
    while True:
        num += 1
        yield num
        sleep(1)

def my_inc():
    global num
    def inner():
        global num
        num += 1
        return num
    return inner

# Create the Gradio interface
with gr.Blocks() as app:

    with gr.Tab("Llamafile Manager"):
        gr.Markdown("# Llamafile Manager")
        gr.Textbox(value = my_inc(), label = "Seconds", interactive=False, every=1)


    with gr.Tab("List Llamafiles"):
        gr.Markdown("List all Llamafiles")
        gr.Button("List Llamafiles").click(list_llamafiles, [], gr.Textbox(label="Llamafiles"))

    with gr.Tab("Check Llamafile"):
        gr.Markdown("Check if a Llamafile exists")
        name_input = gr.Textbox(label="Llamafile Name")
        gr.Button("Check").click(has_llamafile, [name_input], gr.Textbox(label="Exists"))

    with gr.Tab("Download Llamafile"):
        gr.Markdown("Download a Llamafile")
        url_input = gr.Textbox(label="URL")
        name_input_download = gr.Textbox(label="Name")
        gr.Button("Download").click(download_llamafile, [url_input, name_input_download], gr.Textbox(label="Status"))

    with gr.Tab("Download Progress"):
        gr.Markdown("Check Download Progress")
        url_input_progress = gr.Textbox(label="URL")
        name_input_progress = gr.Textbox(label="Name")
        gr.Button("Check Progress").click(download_progress, [url_input_progress, name_input_progress], gr.Textbox(label="Progress"))

    with gr.Tab("Run Llamafile"):
        gr.Markdown("Run a Llamafile")
        name_input_run = gr.Textbox(label="Name")
        args_input_run = gr.Textbox(label="Args (space-separated)")
        gr.Button("Run").click(run_llamafile, [name_input_run, args_input_run], gr.Textbox(label="Run Status"))

iface = app
