from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
from utils.tools import TOOLS

# Load environment variables
load_dotenv()

# Check for GROQ API key
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key or groq_api_key == "YOUR_GROQ_API_KEY_HERE":
    print("❌ GROQ_API_KEY not found or not set!")
    print("🔧 To fix this issue:")
    print("   1. Get your free API key from: https://console.groq.com/")
    print("   2. Set the environment variable:")
    print("      - Windows: set GROQ_API_KEY=your_actual_api_key_here")
    print("      - Linux/Mac: export GROQ_API_KEY=your_actual_api_key_here")
    print("   3. Or create a .env file with: GROQ_API_KEY=your_actual_api_key_here")
    print()
    print("🚀 Alternative: Use the demo mode for testing without API key")
    print("   Run: python demo_sequential_simple.py")
    print()
    raise ValueError("GROQ_API_KEY is required but not set. Please set your API key to continue.")

# Initialize Groq LLM
llm = ChatGroq(
    temperature=0,
    model_name="openai/gpt-oss-20b",
    groq_api_key=groq_api_key
)

# Bind tools to the model
llm_with_tools = llm.bind_tools(TOOLS)