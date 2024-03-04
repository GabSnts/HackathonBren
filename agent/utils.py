import os
from dotenv import load_dotenv
from langchain_community.tools.tavily_search import TavilySearchResults

load_dotenv()

def search_travily():
    os.getenv("TAVILY_API_KEY")
    search = TavilySearchResults()
    return [search]
 