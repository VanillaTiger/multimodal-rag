import os

def read_openai_api_key_to_environ():
    # Read the API key from secrets.txt
    with open('secrets/secrets.txt', 'r') as file:
        api_key = file.readline().strip()

    os.environ["OPENAI_API_KEY"] = api_key