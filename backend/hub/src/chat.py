from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.memory import ChatMessageHistory

history = ChatMessageHistory()

chat = ChatOpenAI(temperature=0,
                  openai_api_key="KEY",
                  base_url="http://localhost:8080/v1")

messages = [
    SystemMessage(
        content="You are a helpful assistant. You keep answers short and to the point. You do not add any extra information. For example, if you are asked how to accomplish a command line task, you reply with the command to use with not additional comments."
    ),
    HumanMessage(
        content="Who wrote Linux?"
    ),
    SystemMessage(
        content="Linus Torvalds"
    ),
    HumanMessage(
        content="When?"
    ),
    SystemMessage(
        content="1991"
    ),
    HumanMessage(
        content="What is the capital of France?"
    ),
    SystemMessage(
        content="Paris"
    ),
    HumanMessage(
        content="How do I add a git origin?"
    ),
    SystemMessage(
        content="git remote add <origin_name> <origin_url>"
    ),
    HumanMessage(
        content="How do I find the process on a port (in Linux)?"
    ),
    SystemMessage(
        content="lsof -i :<port_number>"
    ),
]

while True:
    user_input = input("> ")
    if user_input.lower() == "exit":
        break
    message = HumanMessage(content=f"{user_input}")
    messages.append(message)
    prompt = ChatPromptTemplate.from_messages(messages)
    chain = prompt | chat | StrOutputParser()
    response = chain.invoke({})
    print(response)
    messages.append(SystemMessage(content=response))
