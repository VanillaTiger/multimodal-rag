from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

def load_documents_from_csv():
    # Initialize the CSVLoader with the path to your CSV file
    loader = CSVLoader(file_path='data_img_str_url.csv',metadata_columns=['images','article_url'])

    # Load the documents
    documents = loader.load()

    return documents

def print_first_loaded_document():

    documents = load_documents_from_csv()

    # Print the loaded documents
    for doc in documents:
        print(doc)
        break

def create_db():
    
    documents = load_documents_from_csv()
    
    
    #splitting the text into
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # Embed and store the texts
    # Supplying a persist_directory will store the embeddings on disk
    persist_directory = 'db'

    ## here we are using OpenAI embeddings but in future we will swap out to local embeddings
    embedding = OpenAIEmbeddings()

    vectordb = Chroma.from_documents(documents=texts, 
                                    embedding=embedding,
                                    persist_directory=persist_directory)
    
    # persiste the db to disk
    vectordb.persist()
    vectordb = None

def load_db():
    # Load the vector store from disk
    persist_directory = 'db'

    ## here we are using OpenAI embeddings but in future we will swap out to local embeddings
    embedding = OpenAIEmbeddings()
    
    # Now we can load the persisted database from disk, and use it as normal. 
    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding)
    
    return vectordb
