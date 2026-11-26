from langchain_ollama import ChatOllama

def get_llm():
    """Returns the LLM client"""
    llm = ChatOllama(model="llama3:latest", temperature=0)
    return llm
