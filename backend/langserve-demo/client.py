#!/usr/bin/env python3

from langserve import RemoteRunnable

remote_chain = RemoteRunnable("http://localhost:8800/agent/")
response = remote_chain.invoke({
    "input": "Hello, how are you?",
    "chat_history": []  # Providing an empty list as this is the first call
})

# Parse json response, then get the 'output' key
print(response["output"])
