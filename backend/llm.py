import os
from dotenv import load_dotenv
from persist_dir_delete import delete_directory
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_chroma import Chroma

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
PERSIST_DIRECTORY = './docs/chroma'

# Initialize LLM and embeddings
llm = GoogleGenerativeAI(
    model="gemini-pro",
    google_api_key=GOOGLE_API_KEY
)

embeddings = GoogleGenerativeAIEmbeddings(
    model="models/embedding-001",
    google_api_key=GOOGLE_API_KEY
)

# Load and split document
def load_document_and_split(document):
    loader = PyPDFLoader(document)
    pages = loader.load_and_split()
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=10000,
        chunk_overlap=1000
    )
    texts = text_splitter.split_documents(pages)
    return texts

# Embed documents
def embed_documents(context, persist_directory=PERSIST_DIRECTORY):
    # Ensure the directory is deleted if it exists
    delete_directory(persist_directory)
    # Create a new Chroma instance
    vectordb = Chroma.from_documents(
        documents=context,
        embedding=embeddings,
        persist_directory=persist_directory
    )
    return vectordb

# Set up retrieval chain
def setup_retrieval_chain(vectordb):
    template = """Use the following pieces of context to answer the question at the end you can use the previous chat history as reference If the question is out of the context say I don't know, just say that you don't know, don't try to make up an answer. Keep the answer as concise as possible. Always say "thanks for asking!" at the end of the answer.
    {context}
    Question: {question}
    Helpful Answer:"""

    PROMPT = PromptTemplate.from_template(template)

    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
        output_key='answer'
    )
    print(memory)

    qa = ConversationalRetrievalChain.from_llm(
        llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 5}),
        memory=memory,
        return_source_documents=True,
        return_generated_question=True,
        verbose=False
    )
    return qa

# Handle chat interaction
def handle_chat(qa, question):
    result = qa({"question": question})
    print (result)
    return result['answer']
