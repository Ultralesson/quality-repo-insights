from langchain_openai import ChatOpenAI


def gpt_4o_mini_llm(temperature=0.7):
    return ChatOpenAI(model="gpt-4o-mini", temperature=temperature)
