# Python Llamafile Manager

A python program that downloads and executes [llamafiles](https://github.com/Mozilla-Ocho/llamafile), bundled with [PyInstaller](https://pyinstaller.org/en/stable/).

## Why?

I wrote a python program using `langchain` that assumes an LLM model is exposed somewhere via HTTP. `Llamafile`s are portable executable that expose an HTTP interface to LLMs. Rather than asking users to download and run `Llamafiles`, I want my python program to manage this on their behalf. I plan to bundle my python program with `PyInstaller`, so I will make sure that `python-llamafile-manager` can be bundled with `PyInstaller` too.

## Usage

From within this directory, build with:

``` sh
docker build -f Dockerfile.plm -t memory-cache/python-llamafile-manager .
```

Run with:

``` sh
docker run \
  --name python-llamafile-manager \
  -it \
  --rm \
  -e LLAMAFILE_BIN_DIR=/usr/src/app/bin \
  -v ~/media/llamafile/:/usr/src/app/bin/ \
  -v ./:/usr/src/app/ \
  -p 8800:8800 \
  memory-cache/python-llamafile-manager \
  python3 manager.py
```

## Packaging with PyInstaller

### GNU/Linux

> GNU/Linux
> 
> PyInstaller requires the ldd terminal application to discover the shared libraries required by each program or shared library. It is typically found in the distribution-package glibc or libc-bin.
> 
> It also requires the objdump terminal application to extract information from object files and the objcopy terminal application to append data to the bootloader. These are typically found in the distribution-package binutils.


``` sh
docker build -f Dockerfile.plm-gnu-linux-builder -t memory-cache/plm-gnu-linux-builder .
```

``` sh
```

