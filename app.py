#import
import os
from dotenv import load_dotenv
from ingest import ingest_text
from scraper import scrape_nasa_page
# import streamlit
import streamlit as st
from nasasearch import find_best_source 
from nasasearch import search_wikipedia 
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage
from extractentity import extract_entity
from scraper import scrape_wikipedia_page
#load environment variables
load_dotenv()  

SCRAPERS = {
    "NASA": scrape_nasa_page,
    "Wikipedia": scrape_wikipedia_page
}
embeddings = OllamaEmbeddings(
    model=os.getenv("EMBEDDING_MODEL"),
)

vector_store = Chroma(
    collection_name=os.getenv("COLLECTION_NAME"),
    embedding_function=embeddings,
    persist_directory=os.getenv("DATABASE_LOCATION"), 
)


llm = init_chat_model(
    os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)
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
    entity = extract_entity(user_question, llm).strip().title()
    print("Extracted Entity:", entity)
    result = find_best_source(entity)
    if result is None:
        st.error("No trusted source found.")
        st.stop()
    url = result["url"]
    source = result["source"]
    print("Source:", source)
    print("URL:", url)
    existing = vector_store.get(where={"title": entity})
    if len(existing["ids"]) == 0:
        print("Planet not found in archive")
        print("Scraping:", entity)
        raw_text = SCRAPERS[source](url)
    if (source == "NASA"and (raw_text is None or len(raw_text.split()) < 600) ):
        print("NASA page too small. Switching to Wikipedia...")
        wiki = search_wikipedia(entity)
        if wiki:
            url = wiki["url"]
            source = wiki["source"]
            raw_text = scrape_wikipedia_page(url)
            print("Wikipedia URL:", url)
        if raw_text:
            print("Characters:", len(raw_text))
            print(raw_text[:500])
            ingest_text(raw_text,url,entity,source)
            print("Added", entity, "to archive")
    else:
        print(f"{entity} already exists in archive.")
    docs = vector_store.similarity_search(user_question, k=6)
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
