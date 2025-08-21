from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser

promt = ChatPromptTemplate(
    [
        ("system","you are AI assist bot, please respond to user questions"),
        ("user","Question:{question}")
    ]
)

input_text = input("ask your question: ")
llm = OllamaLLM(model="deepseek-r1:1.5b")
output_parser = StrOutputParser()

chain = promt|llm|output_parser
if input_text:
    print(chain.invoke({'question':input_text}))

