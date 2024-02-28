from langchain_community.chat_models import ChatOllama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOllama(model="mixtral:8x7b-instruct-v0.1-fp16")
llm.base_url = "http://localhost:11434"
prompt = ChatPromptTemplate.from_template("Tell me a short joke about {topic}")
chain = prompt | llm | StrOutputParser()
print(chain.invoke({"topic": "Space travel"}))
