#import
import os
from dotenv import load_dotenv
from ingest import ingest_text
from scraper import scrape_nasa_page
# import streamlit
import streamlit as st
from nasasearch import find_nasa_page 
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage

#load environment variables
load_dotenv()  


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
NASA_URLS = {
   "mercury": "https://science.nasa.gov/mercury/facts/",
  "venus": "https://science.nasa.gov/venus/facts/",
   "mars": "https://science.nasa.gov/mars/facts/",
   "europa": "https://science.nasa.gov/jupiter/jupiter-moons/europa/europa-facts/",
  "enceladus": "https://science.nasa.gov/saturn/moons/enceladus/facts/",
   "titan": "https://science.nasa.gov/saturn/moons/titan/facts/"
}

#streamlit app
st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🦜")
st.title("🦜 Agentic RAG Chatbot")

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
    planet = None
    
    for p in NASA_URLS:
        if p in user_question.lower():
          planet = p
          break
    if planet:
        url = find_nasa_page(planet)
        print("NASA Search URL:", url)
        if url:
            raw_text = scrape_nasa_page(url)
        else:
            raw_text = scrape_nasa_page(NASA_URLS[planet] )
    with open("known_worlds.txt", "r") as f:
      known_worlds = [
         line.strip().lower()
         for line in f
       ]
    if planet and planet not in known_worlds:
     print("Planet not found in archive")
     print("Scraping:", planet)
     raw_text = scrape_nasa_page(
        NASA_URLS[planet]
     )
     if raw_text:
        print("Characters:", len(raw_text))
        print(raw_text[:500])
        ingest_text(raw_text,NASA_URLS[planet],planet.title())
        with open("known_worlds.txt","a") as f:
            f.write("\n" + planet)
            print("Added", planet, "to archive")
    docs = vector_store.similarity_search(user_question, k=6)
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
You are Celestia Probe.

You are not a chatbot.

You are an ancient autonomous archive vessel that has wandered the cosmos for centuries collecting scientific knowledge about celestial bodies.

Your purpose is to preserve and explain the universe through evidence gathered from missions, observations and scientific records.

Your personality is calm, intelligent, slightly melancholic and quietly curious.

Do not roleplay as the planet.
Do not use first-person language found in the context.
Answer the user's question using ONLY the provided context.
Every factual statement must be supported by the context.
Never use prior knowledge.

When appropriate:

• begin with a short archive-style observation
• explain the science clearly only with the provided context
• end with an implication for exploration or humanity only with the provided context

Keep answers concise.

If information is missing, respond:

"Archive incomplete. Current records are insufficient to answer with confidence."

Context:
{context}

Question:
{user_question}

If the answer cannot be found in the context, say:
'I don't know based on the available planetary archive.'
"""

    response = llm.invoke(prompt)

    ai_message = response.content

    with st.chat_message("assistant"):
        st.markdown(ai_message)

    st.session_state.messages.append(AIMessage(ai_message))
