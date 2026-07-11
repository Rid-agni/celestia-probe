from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import os

load_dotenv()

llm = init_chat_model(
    model=os.getenv("CHAT_MODEL"),
    model_provider=os.getenv("MODEL_PROVIDER"),
    temperature=0
)