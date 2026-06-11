import streamlit as st
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

@st.cache_resource
def load_retriever():
    loaders = [
        TextLoader("faq.txt"),
        TextLoader("business.txt"),
        PyPDFLoader("sixt_US_Rental.pdf"),
    ]
    docs = []
    for loader in loaders:
        docs.extend(loader.load())

    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectorstore = FAISS.from_documents(chunks, embedding=embeddings)
    return vectorstore.as_retriever(search_kwargs={"k": 3})

def ask_sixt_assistant(question):
    retriever = load_retriever()
    results = retriever.invoke(question)
    answer = results[0].page_content if results else "I don't have that information."
    sources = [doc.page_content[:150] for doc in results]
    return answer, sources
