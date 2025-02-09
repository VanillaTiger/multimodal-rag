from langchain_community.document_loaders import CSVLoader
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import argparse
from loguru import logger

from src.utils.utils import read_openai_api_key_to_environ

def load_documents_from_csv():
    """
    Load the documents from the CSV file
    """
    # Initialize the CSVLoader with the path to your CSV file
    loader = CSVLoader(file_path='data/data_img_str_url.csv',metadata_columns=['images','article_url', 'title'])

    # Load the documents
    documents = loader.load()
    logger.info(f"Loaded {len(documents)} documents from CSV")

    return documents

def print_first_loaded_document():
    """
    Print the first loaded document
    """

    documents = load_documents_from_csv()

    # Print the loaded documents
    for doc in documents:
        print(doc)
        break

def create_db():
    """
    create the database in local directory
    """
    
    read_openai_api_key_to_environ()
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
    
    logger.info(f"Database created successfully in {persist_directory}")

def load_db():
    """
    Load the database from local directory
    """
    # Load the vector store from disk
    persist_directory = 'db'

    ## here we are using OpenAI embeddings but in future we will swap out to local embeddings
    embedding = OpenAIEmbeddings()
    
    # Now we can load the persisted database from disk, and use it as normal. 
    vectordb = Chroma(persist_directory=persist_directory, 
                    embedding_function=embedding)
    
    logger.info(f"Database loaded successfully from {persist_directory}")
    
    return vectordb

def parse_args():
    parser = argparse.ArgumentParser(description="Database Manager")
    parser.add_argument('--create_db', action='store_true', help='Create the database')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()

    if args.create_db:
        create_db()