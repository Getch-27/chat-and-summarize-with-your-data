import os
from dotenv import load_dotenv
from persist_dir_delete import delete_directory
import numpy as np

#Gemini llm
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings

#document and text
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain

#prompt and retrival
from langchain.prompts import PromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_chroma import Chroma
load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
document = "Retrieval-Augmented Generation for.pdf"
persist_directory = './docs/chroma'

llm = ChatGoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY
    )

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
     google_api_key=GOOGLE_API_KEY
    )

## Document loading and splitting
def load_document_and_split(document):
    loader = PyPDFLoader(document)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = 10000,
        chunk_overlap = 100
    )
    texts = text_splitter.split_documents(pages)
    return texts

context = load_document_and_split(document)

## vectors and embadding
delete_directory(persist_directory)

vectordb = Chroma.from_documents(
    documents=context,
    embedding=embeddings,
    persist_directory=persist_directory
)
question = "what is RAG?"
doc = vectordb.similarity_search(question , k=8)
print(doc)