import streamlit as st
from langchain_openai.chat_models import ChatOpenAI

from components.sidebar import sidebar

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

with st.form("my_form"):
    text = st.text_area(
        "Enter text:",
        "What are the three key pieces of advice for learning how to code?",
    )
    submitted = st.form_submit_button("Submit")
    if not st.session_state["OPENAI_API_KEY"].startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")
    if submitted and st.session_state["OPENAI_API_KEY"].startswith("sk-"):
        generate_response(text)

with st.expander("Advanced Options"):
    return_all_chunks = st.checkbox("Show all chunks retrieved from vector search")
    show_full_doc = st.checkbox("Show parsed contents of the document")
