import sys
from retrieval import get_response
from utils.utils import read_openai_api_key_to_environ

def print_response(response):
    for key,value in response.items():
        print(key, "\n", value , "\n")

def main():

    read_openai_api_key_to_environ()

    if len(sys.argv) < 2:
        print("Please provide an input query.")
        return

    query = sys.argv[1]
    response = get_response(query)
    print_response(response)

if __name__ == "__main__":
    main()