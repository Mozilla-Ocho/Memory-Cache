# Memory Cache Hub

A backend for Memory Cache built on [langchain](https://python.langchain.com/), bundled as an executable with [PyInstaller](https://pyinstaller.org/). 

## Overview

The `hub` is a central component of Memory Cache:

- It exposes APIs used by `browser-extension`, `browser-client`, and plugins.
- It serves the static `browser-client` files over HTTP.
- It downloads `llamafile`s and runs them as subprocesses.
- It interacts with a vector database to ingest and retrieve document fragments.
- It synthesizes queries and prompts for backend `llm`s on behalf of the user.

## How to Develop

A development environment for working on `hub` is provided by the Dockerfile `docker/Dockerfile.hub-dev`. 

The basic workflow is to build this image and then bind mount the source code when you run the container. You will also want to bind mount a `LLAMAFILES_DIR` pointing to a directory where you'll store `llamafile`s. These can be quite large, so we avoid re-downloading them every time we start the container.

When you are satisfied with development, you will want to package the `hub` as an executable with `PyInstaller`. Since `PyInstaller` does not support cross-compilation, you will need to run the build commands on the platform you are targeting. For example, to build a MacOS executable, you will need to run the build commands on a MacOS machine. 

Examples of how to build and use the development and builder images are provided in the sections below.

## Development

Build the development image:

```bash
docker build -f docker/Dockerfile.hub-dev -t memory-cache/hub-dev .
```

Run the development container:

```bash
docker run -it --rm \
  -v $(pwd):/hub \
  -v ~/media/llamafile:/llamafiles \
  -e LLAMAFILES_DIR=/llamafiles \
  memory-cache/hub-dev
```

Replace `~/media/llamafile` with the path to the directory where you want to store `llamafile`s.

## Building for GNU/Linux

Build the builder image:

```bash
docker build -f docker/Dockerfile.hub-builder-gnu-linux -t memory-cache/hub-builder-gnu-linux .
```

Run the builder container:

```bash
docker run -it --rm \
  -v $(pwd):/hub \
  memory-cache/hub-builder-gnu-linux
```

The builder will generate `memory-cache-hub-gnu-linux` in the `dist` directory.

## Building for MacOS

On MacOS, we use a python virtual environment to install the dependencies and run the build commands.

Create the virtual environment:

```bash
python3.11 -m venv venv
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements/hub-base.txt \
    -r requirements/hub-cpu.txt \
    -r requirements/hub-builder.txt
```

Build the executable:
    
```bash
python3.11 src/hub_build_macos.py
```

The builder will generate `memory-cache-hub-macos` in the `dist` directory.

When you are done, deactivate the virtual environment:

``` sh
deactivate
```

If you want to remove the virtual environment, just delete the `venv` directory.


## Plan/TODO

- [ ] Write Hello World server
- [ ] Bundle with PyInstaller on Linux
- [ ] Bundle with PyInstaller on MacOS
- [ ] Bundle with PyInstaller on Windows
- [ ] Test NVIDIA w/ CUDA
- [ ] Test AMD w/ HIP/Rocm
- [ ] Test x86-64
- [ ] Test Apple silicon
- [ ] Add llamafile management
- [ ] Add ingestion
- [ ] Add retrieval
- [ ] Connect to browser client

## Miscellaneous Notes

### `python 3.11`

We use `python 3.11` (not `3.12` or later)  because `faiss-cpu` only supports up to `3.11` at the time of this writing: https://pypi.org/project/faiss-cpu/
