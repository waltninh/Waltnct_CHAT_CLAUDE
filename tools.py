import math
from dotenv import load_dotenv
from langchain_core.tools import tool
from langchain_tavily import TavilySearch


load_dotenv()


web_search = TavilySearch(
    max_results=5,
    topic="general",
    search_depth="advanced"
)
