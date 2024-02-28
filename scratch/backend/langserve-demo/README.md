# Lang Serve Demo

A demo app built with `langchain` and `langserve`.

## Dockerfiles

| Filename                 | Purpose                        |
|:-------------------------|:-------------------------------|
| `Dockerfile.cpu`         | Basic setup. CPU support only. |

## Usage

From within this directory, build with:

``` sh
docker build -f Dockerfile.cpu -t memory-cache/lang-serve-demo-cpu .
```

Save an API key to a file called `openai-api-key` and run:

``` sh
docker run \
  --rm \
  --name lang-serve-demo-cpu \
  -p 8800:8800 \
  -e OPENAI_API_KEY="$(cat openai-api-key)" \
  -v ./:/usr/src/app/ \
  memory-cache/lang-serve-demo-cpu
```

(Note: I'll remove the OpenAI dependency shortly. It's only here because I'm starting with langchain's demo server.)

Then run a client to interact with the server:

``` sh
docker exec lang-serve-demo-cpu python client.py 
```


## Miscellaneous Notes

### Dockerfile.cpu: `python 3.11`

We use `python 3.11` (not `3.12` or later)  in `Dockerfile.cpu` because `faiss-cpu` only supports up to `3.11` at the time of this writing: https://pypi.org/project/faiss-cpu/




