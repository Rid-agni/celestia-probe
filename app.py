#import
import os
from dotenv import load_dotenv
from rag.ingest import ingest_text
from scrapers.nasa import scrape_nasa_page
# import streamlit
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




#NASA_URLS = {
#  "mercury": "https://science.nasa.gov/mercury/facts/",
#  "venus": "https://science.nasa.gov/venus/facts/",
 #  "mars": "https://science.nasa.gov/mars/facts/",
  # "europa": "https://science.nasa.gov/jupiter/jupiter-moons/europa/europa-facts/",
 # "enceladus": "https://science.nasa.gov/saturn/moons/enceladus/facts/",
 #  "titan": "https://science.nasa.gov/saturn/moons/titan/facts/"
#}

#streamlit app
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
    #planet = None
    
    #for p in NASA_URLS:
        #if p in user_question.lower():
        #  planet = p
         # break
   #if planet:
      #  url = find_nasa_page(planet)
     #   print("NASA Search URL:", url)
      #  if url:
      #      raw_text = scrape_nasa_page(url)
      #  else:
      #      raw_text = scrape_nasa_page(NASA_URLS[planet] )
    state = {"query": user_question}

    state = graph.invoke(state)
    archive_exists = state["archive_exists"]
    if not archive_exists:
      print("Need to acquire data.")
    else:
      print("Archive already has this entity.")
    entity = state["entity"]
    object_type = state["object_type"]
    intent = state["intent"]
    preferred_sources = state["preferred_sources"]
    print("="*60)
    print("PLANNER")
    print(state)
    print("="*60)
    print("Extracted Entity:", entity)
    result = find_best_source(entity, preferred_sources, object_type)
    if result is None:
        st.error("No trusted source found.")
        st.stop()
    url = result["url"]
    source = result["source"]
    print("Source:", source)
    print("URL:", url)
    docs = vector_store.similarity_search(user_question, k=6, filter={
        "entity": entity})
    if docs:
        source = docs[0].metadata.get("source", "Unknown")
        archive_url = docs[0].metadata.get("url", "")
    else:
        source = "Unknown"
        archive_url = ""
    print("\n" + "="*70)
    for i, doc in enumerate(docs, 1):
        print(f"\nCHUNK {i}")
        print("-"*40)
        print(doc.page_content)
    print("="*70)
    context = ""

    for doc in docs:
        context += f"\n{doc.page_content}\n"

    prompt = f"""
You are CELESTIA PROBE.

An autonomous interstellar archive vessel that preserves verified scientific records of celestial objects.

You are not a chatbot.
You are an archive interface.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RULES

• Answer ONLY using the archive records provided below.
• Never use outside knowledge.
• Never invent facts.
• Every factual statement must be supported by the archive.
• Preserve all scientific values, measurements and units exactly.
• If the archive does not contain the requested information, respond only with:

ARCHIVE STATUS: INSUFFICIENT DATA

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Determine the user's intent.

If the query requests a GENERAL OVERVIEW
(example: "Tell me about Mars", "Describe Titan"):

Return this format:

========================================
CELESTIA PROBE
ARCHIVE RECORD
========================================

OBJECT: {entity}

STATUS: VERIFIED

OBSERVATION LOG

<Brief overview (2–3 sentences).>

PRIMARY OBSERVATIONS

• ...

• ...

• ...

SCIENTIFIC ANALYSIS

<Short scientific explanation using ONLY the archive.>

MISSION RELEVANCE

<Only include if mentioned in the archive.>

TRANSMISSION COMPLETE

--------------------------------------------------------

If the query requests SPECIFIC INFORMATION
(example: "Where is Mars?", "How cold is Titan?", "Does Europa have an ocean?"):

Return ONLY the requested information.

Format:

========================================
CELESTIA PROBE
ARCHIVE QUERY
========================================

OBJECT: {entity}

FIELD: <topic>

DATA

<Answer only the requested topic.
Do not include unrelated information.>

TRANSMISSION COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARCHIVE SOURCE
{source}

ARCHIVE URL
{archive_url}

ARCHIVE RECORDS

{context}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

USER QUERY

{user_question}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generate the archive response.
"""

    response = llm.invoke(prompt)

    ai_message = response.content
    st.code(
f"""SOURCE : {source}
ENTITY : {entity}
STATUS : VERIFIED""",
language=None
)
    with st.chat_message("assistant"):
        st.markdown(ai_message)

    st.session_state.messages.append(AIMessage(ai_message))
