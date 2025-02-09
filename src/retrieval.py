from src.db_manager import load_db
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_core.tracers.context import tracing_v2_enabled

## Cite sources
def process_llm_response(llm_response):
    result = {}
    sources_list = []
    result["answer"]= llm_response['result']
    for source in llm_response["source_documents"]:
        sources_list.append([source.metadata['source'], source.metadata['row'], source.metadata['article_url'], source.metadata['images'], source.metadata['title']])
    
    result["sources"] = sources_list
    
    return result

def create_retrieval():
    vectordb = load_db()
    retriever =vectordb.as_retriever(search_kwargs={"k": 3})
    # create the chain to answer questions 
    qa_chain = RetrievalQA.from_chain_type(llm=OpenAI(), 
                                    chain_type="stuff", 
                                    retriever=retriever, 
                                    return_source_documents=True)
    
    return qa_chain


def get_response(query, qa_chain):
    with tracing_v2_enabled():
        # query = "Who is Mustafa Suleyman?"
        llm_response = qa_chain.invoke(query)
        result = process_llm_response(llm_response)

    return result