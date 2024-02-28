from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import SQLChatMessageHistory
from langchain_openai import ChatOpenAI

# This is where we configure the session id
config = {"configurable": {"session_id": "test_session_id2"}}

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chat = ChatOpenAI(temperature=0,
                  openai_api_key="KEY",
                  base_url="http://localhost:8080/v1")

chain = prompt | chat
chain_with_history = RunnableWithMessageHistory(
    chain,
    lambda session_id: SQLChatMessageHistory(
        session_id=session_id, connection_string="sqlite:///sqlite.db"
    ),
    input_messages_key="question",
    history_messages_key="history",
)

print(chain_with_history.invoke({"question": "Whats my name"}, config=config))
