import os
from langchain_community.tools.tavily_search import TavilySearchResults

def search_travily():
    os.environ["TAVILY_API_KEY"] = "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"
    search = TavilySearchResults()
    return [search]
 