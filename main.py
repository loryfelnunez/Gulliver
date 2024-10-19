import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

from components.sidebar import sidebar
from core import index

from ui import (
    is_query_valid,
    is_open_ai_key_valid,
)

st.set_page_config(page_title="Gulliver's Digest", page_icon="📖", layout="wide")
st.header("📖Gulliver's Digest")


# Enable caching for expensive functions

#bootstrap_caching()

sidebar()

def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=st.session_state["OPENAI_API_KEY"] )
    st.info(model.invoke(input_text))



with st.form("Query Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")
    arxiv_date_start = st.date_input("Give start date of articles", value=None)
    arxiv_date_end =  st.date_input("Give end date of articles", value=None)
    text = st.text_area(
        "Enter text:",
        "Summarize the articles for me",
    )
    submitted = st.form_submit_button("Submit")
    index.index_query(arxiv_date_start, arxiv_date_end, text)
    if not st.session_state["OPENAI_API_KEY"].startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and st.session_state["OPENAI_API_KEY"].startswith("sk-"):
        generate_response(text)


# with st.spinner("Indexing document... This may take a while⏳"):
#     folder_index = embed_files(
#         files=[chunked_file],
#         embedding=EMBEDDING if model != "debug" else "debug",
#         vector_store=VECTOR_STORE if model != "debug" else "debug",
#         openai_api_key=openai_api_key,
#     )
