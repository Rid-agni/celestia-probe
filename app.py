import os
from dotenv import load_dotenv
from rag.ingest import ingest_text
from scrapers.nasa import scrape_nasa_page
import streamlit as st
from search.search import find_best_source 
from search.search import search_wikipedia 
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from search.extract_entity import extract_entity
from planner import planner_agent
from agents.planner import planner_node
from graph import graph
from rag.vectorstore import vector_store
from config import llm
from scrapers.wikipedia import scrape_wikipedia_page
#load environment variables
load_dotenv()  

SCRAPERS = {
    "NASA": scrape_nasa_page,
    "Wikipedia": scrape_wikipedia_page
}

#streamlit
st.set_page_config(page_title="Celestia Probe", page_icon="🖥️")
st.title("Celestia Probe")

# initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# display chat messages from history on app rerun
for message in st.session_state.messages:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    elif isinstance(message, AIMessage):
        with st.chat_message("assistant"):
            st.markdown(message.content)


#message bar 
user_question = st.chat_input("Enter celestial object")

if user_question:

    with st.chat_message("user"):
        st.markdown(user_question)

    st.session_state.messages.append(HumanMessage(user_question))
    state = {"query": user_question}

    state = graph.invoke(state)
    archive_exists = state["archive_exists"]
    docs = state["docs"]
    source = state["source"]
    archive_url = state["archive_url"]
    entity = state["entity"]
    object_type = state["object_type"]
    intent = state["intent"]
    preferred_sources = state["preferred_sources"]
    ai_message = state["answer"]
    source = state["source"]
    archive_url = state["archive_url"]
    print("="*60)
    print("GRAPH STATE")
    print(state)
    print("="*60)
    print("Extracted Entity:", entity)
    st.code(
f"""SOURCE : {source}
ENTITY : {entity}
STATUS : VERIFIED""",
language=None
)
    with st.chat_message("assistant"):
        st.markdown(ai_message)

    st.session_state.messages.append(AIMessage(ai_message))