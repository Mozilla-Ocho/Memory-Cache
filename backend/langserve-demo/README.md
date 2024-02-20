# Memory Cache Backend

A backend for Memory Cache built on [langchain](https://python.langchain.com/) and bundled as an executable with [PyInstaller](https://pyinstaller.org/). 

## Plan/TODO

- [x] Write langchain Hello World server
- [ ] Bundle with PyInstaller on Linux
- [ ] Bundle with PyInstaller on MacOS
- [ ] Bundle with PyInstaller on Windows
- [ ] Test NVIDIA w/ CUDA
- [ ] Test AMD w/ HIP/Rocm
- [ ] Test x86-64
- [ ] Test Apple silicon
- [ ] Add doc db and RAG

## Dockerfiles

| Filename                 | Purpose                        |
|:-------------------------|:-------------------------------|
| `Dockerfile.cpu`         | Basic setup. CPU support only. |
| [TODO] `Dockerfile.cuda` | NVIDIA CUDA support.           |

## Usage

From within this directory, build with:

``` sh
docker build -f Dockerfile.cpu -t memory-cache/cpu-backend .
```

Save an API key to a file called `openai-api-key` and run:

``` sh
docker run \
  --rm \
  --name memory-cache-backend \
  -p 8800:8800 \
  -e OPENAI_API_KEY="$(cat openai-api-key)" \
  -v ./:/usr/src/app/ \
  memory-cache/cpu-backend
```

(Note: I'll remove the OpenAI dependency shortly. It's only here because I'm starting with langchain's demo server.)

Then run a client to interact with the server:

``` sh
docker exec memory-cache-backend python client.py 
```



## Miscellaneous Notes

### Dockerfile.cpu: `python 3.11`

We use `python 3.11` (not `3.12` or later)  in `Dockerfile.cpu` because `faiss-cpu` only supports up to `3.11` at the time of this writing: https://pypi.org/project/faiss-cpu/

### Dockerfile.cpu: `python 3.10`

We use `python 3.10` (not `3.11` or later)  in `Dockerfile.cuda` because `faiss-gpu` only supports up to `3.10` at the time of this writing: https://pypi.org/project/faiss-gpu/

### git diff

View the relevant diff on github, here: https://github.com/Mozilla-Ocho/Memory-Cache/compare/browser-client...johnshaughnessy:Memory-Cache:backend?expand=1




