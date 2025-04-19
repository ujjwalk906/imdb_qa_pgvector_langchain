from langchain.chains.summarize import load_summarize_chain
from langchain_openai import ChatOpenAI

def summarize_docs(docs):
    llm = ChatOpenAI(temperature=0.3)
    chain = load_summarize_chain(llm, chain_type="stuff")
    return chain.run(docs)
