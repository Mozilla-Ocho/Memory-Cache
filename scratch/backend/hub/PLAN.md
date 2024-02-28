# Memory Cache Hub

The `hub` is a central component of Memory Cache:

- It exposes APIs used by `browser-extension`, `browser-client`, and plugins.
- It serves the static `browser-client` files over HTTP.
- It downloads `llamafile`s and runs them as subprocesses.
- It interacts with a vector database to ingest and retrieve document fragments.
- It synthesizes queries and prompts for backend `llm`s on behalf of the user.

## Control Flow

When `memory-cache-hub` starts, it should:
- Check whether another instance of `memory-cache-hub` is already running. If it is, log an error and exit.
- Start the FastAPI server. If the port is already in use, log an error and exit.

From then on, everything is driven by API requests.

## API Endpoints

| Route                                    | Method | Summary                                     |
|:-----------------------------------------|:-------|:--------------------------------------------|
| `/api/llamafile/list`                    | GET    | List available llamafiles                   |
| `/api/llamafile/run`                     | POST   | Run a llamafile                             |
| `/api/llamafile/stop`                    | POST   | Stop a running llamafile                    |
| `/api/llamafile/get`                     | GET    | Get information about a llamafile           |
| `/api/llamafile/download`                | POST   | Initiate download of a llamafile            |
| `/api/llamafile/delete`                  | POST   | Delete a llamafile                          |
| `/api/llamafile/check_download_progress` | POST   | Check download progress of a llamafile      |
| `/api/threads/list`                      | GET    | List chat threads                           |
| `/api/threads/get`                       | GET    | Get information about a chat thread         |
| `/api/threads/create`                    | POST   | Create a new chat thread                    |
| `/api/threads/delete`                    | POST   | Delete a chat thread                        |
| `/api/threads/send_message`              | POST   | Send a message to a chat thread             |
| `/api/threads/rag_send_message`          | POST   | Send a message to a chat thread using RAG   |
| `/api/threads/get_messages`              | GET    | Get messages from a chat thread             |
| `/api/threads/config`                    | POST   | Configure a chat thread                     |
| `/api/datastore/ingest`                  | POST   | Ingest document fragments in the data store |
| `/api/datastore/status`                  | GET    | Get status of the data store                |
| `/api/datastore/config`                  | POST   | Configure the data store                    |
| `/api/datastore/config`                  | GET    | Get configuration of the data store         |














