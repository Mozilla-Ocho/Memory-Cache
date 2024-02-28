import subprocess
import os
import stat
import requests
import sys
from tqdm import tqdm
from time import sleep

url_llava_v1_5_7b_q4 = "https://huggingface.co/jartine/llava-v1.5-7B-GGUF/resolve/main/llava-v1.5-7b-q4.llamafile?download=true"

def find_llamafiles(directory: str):
    """Check for files with .llamafile extension in the specified directory."""
    return [file for file in os.listdir(directory) if file.endswith('.llamafile')]

process = None

def execute_llamafile(directory: str, filename: str, args: list):
    """Execute a .llamafile as a subprocess with optional arguments."""
    global process
    filepath = os.path.join(directory, filename)

    # print the file path
    print(filepath)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"{filename} not found in {directory}")

    if not os.access(filepath, os.X_OK):
        raise PermissionError(f"{filename} is not executable")

    print(args)
    print([filepath] + args)

    process = subprocess.Popen([filepath] + args)

def is_process_alive():
    """Check if the subprocess is alive."""
    global process
    return process is not None and process.poll() is None

def stop_process():
    """Stop the subprocess if it is running."""
    global process
    if is_process_alive():
        process.terminate()
        process.wait()

def restart_process(directory: str, filename: str, args: list):
    """Restart the .llamafile subprocess with optional arguments."""
    stop_process()
    execute_llamafile(directory, filename, args)

def download_file_with_tqdm(url: str, destination: str):
    """Download a file from a URL with a progress bar."""
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    block_size = 1024
    with open(destination, 'wb') as file:
        for data in tqdm(response.iter_content(block_size), total=total_size/block_size, unit='KB', unit_scale=True):
            file.write(data)

def download_file(url: str, destination: str):
    """Download a file from a URL."""
    response = requests.get(url)
    with open(destination, 'wb') as file:
        file.write(response.content)

def make_executable_unix(destination: str):
    """Mark a file as executable (Unix-like systems)."""
    os.chmod(destination, os.stat(destination).st_mode | stat.S_IEXEC)

def make_executable_windows(destination: str):
    """Windows-specific handling to 'mark' a file as executable is not applicable."""
    pass  # Windows uses file associations to execute files, so no action needed here.

def download_and_make_executable(url: str, destination: str):
    """Download a file from a URL and mark it as executable."""
    #download_file(url, destination)
    download_file_with_tqdm(url, destination)
    if os.name != 'nt':
        make_executable_unix(destination)
    else:
        make_executable_windows(destination)

# Example usage:
if __name__ == "__main__":
    # Get directory from environment variable or use default
    directory = os.environ.get('LLAMAFILE_BIN_DIR')
    if directory is None:
        # Print error and exit
        print("Error: LLAMAFILE_BIN_DIR environment variable not set")
        sys.exit(1)

    llamafiles = find_llamafiles(directory)
    print("Found llamafiles:", llamafiles)
    if 'foo.llamafile' not in llamafiles:
        response = input("foo.llamafile not found. Do you want to download foo.llamafile? (y/n): ")
        if response.lower() == 'y':
            download_and_make_executable(url_llava_v1_5_7b_q4, os.path.join(directory, 'foo.llamafile'))
        else:
            print("foo.llamafile not found and not downloaded")
            sys.exit(1)
        llamafiles = find_llamafiles(directory)

    if 'foo.llamafile' not in llamafiles:
        print("Error: foo.llamafile not found")
        sys.exit(1)

    execute_llamafile(directory, 'foo.llamafile', ['--host', '0.0.0.0', '--port', '8800'])

    # Check if the process is running every 5 seconds
    while is_process_alive():
        print("foo.llamafile is running")
        sleep(5)
