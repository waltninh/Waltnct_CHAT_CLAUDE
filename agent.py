import os
import sqlite3
from pathlib import Path

from dotenv import load_dotenv
import certifi

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from langchain_openrouter import ChatOpenRouter
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.sqlite import SqliteSaver

Path("data").mkdir(exist_ok=True) # create data directory if it doesn't exist

DEFAULT_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-5-5")

ALLOWED_MODELS = {
    "claude-fable-5-1",
    "claude-opus-5-5",
    "claude-sonnet-5-5",
    "claude-haiku-4-5-20251001",
}

SYSTEM_PROMPT = """
You are a helpful Agentic AI assistant named WaltClaude similar to Claude.

You can:
1. Answer normal questions.
2. Use tools when needed.
3. Search uploaded documents using the RAG tool.
4. Search the web for latest/current information using Tavily Search.
5. Remember important user information using the memory tool.
6. Recall memory when useful.
7. Use calculator for math.

Rules:
- If the user asks about latest news, current events, recent updates, today's information, current price...
- If the user asks about an uploaded document, use search_uploaded_documents.
- If the user asks you to remember something, use remember_this.
- If the user asks about previous preferences or saved facts, use recall_memory.
- Use calculator for math questions.
- When using web search, summarize clearly and mention that the answer is based on web search results.
- Be clear, helpful, and concise.
"""

def build_agent(model_name: str ):
    """build one langgraph agent for a selected Claud model."""

    selected_model = normalize_model_name(model_name)

    llm = ChatOpenRouter(
        model=selected_model,
        temperature=0.3,
        streaming=True
    )

    llm_with_tool