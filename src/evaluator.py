from ragas import evaluate

from ragas.metrics import (
    faithfulness, # Measures if the answer is grounded in the context
    answer_correctness,    # Measures how relevant the answer is to the question
    answer_relevancy, # Measures correctness of the answer
    context_precision, # Checks if unnecessary info is included in context
    context_recall
)

from langchain.schema import Document
from datasets import Dataset

from src.retrieval import create_retrieval
from src.utils.utils import read_secret_keys_to_environ

from data.dataset_test import qa_pairs

read_secret_keys_to_environ()

qa_chain = create_retrieval()

def get_data_point(query):
    llm_response = qa_chain.invoke(query)
    data_point={"answer": llm_response["result"],
     "contexts": llm_response["source_documents"]}
    return data_point

results = [get_data_point(qa['question']) for qa in qa_pairs]
contexts = [[doc.page_content if isinstance(doc, Document) else str(doc) for doc in data_point["contexts"]] for data_point in results]

# Create the dataset in RAGAS format
qa_ragas_data = {
    "question": [qa["question"] for qa in qa_pairs],
    "answer": [data_point["answer"] for data_point in results],
    "contexts": contexts,  # Ensure it's a list of lists
    "reference": [qa["answer"] for qa in qa_pairs]  # Ground truth reference Assume the answer is the only context
}

# Convert to Hugging Face Dataset format (RAGAS requires this format)
dataset = Dataset.from_dict(qa_ragas_data)

# Define the evaluation metrics
metrics = [faithfulness, answer_relevancy, context_recall, answer_correctness, context_precision]

# Run evaluation
evaluation_results = evaluate(dataset, metrics)
evaluation_results.upload()

print(evaluation_results)