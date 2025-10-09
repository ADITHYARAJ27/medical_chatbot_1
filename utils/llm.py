from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from utils.tools import TOOLS

# Load environment variables
load_dotenv()

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-20b",
    groq_api_key=os.getenv("GROQ_API_KEY")
)

# Bind tools to the model
llm_with_tools = llm.bind_tools(TOOLS)