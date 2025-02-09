from src.retrieval import create_retrieval, get_response
import streamlit as st
import time
import pandas as pd

from src.utils.utils import read_openai_api_key_to_environ

read_openai_api_key_to_environ()
qa_chain = create_retrieval()

# Load the CSV file
csv_file = 'data/data_img_str_url.csv'
df = pd.read_csv(csv_file)


# Streamed response emulator
def response_generator(result):
    answer = result["answer"]
    sources = result["sources"]

    response = f"""
    {answer} 
      \n  \n
      \n  \n
    """
    for word in response.split():
        if word =="\n":
            yield "  "+word
        else:
            yield word + " "
        time.sleep(0.05)

def source_generator(sources):

    response = "Sources:   \n  \n"
    
    for source in sources:
        response += f"  \n  \n title = {source[4]}  \n source_file = {source[0]} in row = {source[1]}  \n article_url = {source[2]}  \nimages = {source[3]} \n\n "

    return response

# Set the page layout to wide
st.set_page_config(layout="wide")

chat_tab, data_tab =  st.tabs(["Chat", "Data"])

with chat_tab:
    st.title("The Batch chat")

    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("What do you want to know from The Batch DeepLearning AI?"):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):

            result = get_response(prompt, qa_chain)

            response = st.write_stream(response_generator(result))

            for source in result["sources"]:
                st.write(source_generator([source]))
                st.image(source[3], caption="image associated with the article")
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})

with data_tab:

    st.write("CSV Visualizer")
    st.dataframe(df)  # You can also use st.table(df) for a static table