from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI


def ollama_llm(model="llama3.1", temperature=0.7):
    return OllamaLLM(model=model, temperature=temperature)


def gpt_4o_mini_llm(temperature=0.7):
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
