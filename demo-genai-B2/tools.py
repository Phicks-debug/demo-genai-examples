from modules.core import Tools

from datetime import datetime
import pytz, boto3, json
import wikipedia # type: ignore

import requests
from langchain_community.tools import DuckDuckGoSearchRun

import urllib.parse


@Tools.tool("retrieve", "data")
def call_wolframalpha(query: str) -> str:
    """
    Function to call wolframalpha API
    """
    
    encoded_query = urllib.parse.quote(query)
    
    url = f"https://www.wolframalpha.com/api/v1/llm-api?input={encoded_query}s&appid=AQHXEG-WE9WU4T6K6"
    
    return requests.get(url).text


@Tools.tool("retrieve","data")
def get_time_date() -> str:
    """
    Function to retrive current time day, month and year base on time zone
    """
    
    # Attempt to get the current time in the specified time zone
    tz = pytz.timezone("Asia/Bangkok")
    current_time = datetime.now(tz)

    # Format the time as a string
    return current_time.strftime('%Y-%m-%d %H:%M:%S %Z')


@Tools.tool("retrieve","documents")
def link_to_knowledgebase(query: str) -> json:
    """
    Function to call API to knowledge base and retrieve data source from it.
    
    @param query: The query we want to search for
    
    @return: Compressed json file with chunking base and link-sources
    """
        
    runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    
    # Compress into API POST request to send to knowledge base
    kwargs = {
        "knowledgeBaseId": "AYP6WXNCZ0",
        "retrievalConfiguration": {
            "vectorSearchConfiguration": {
                "numberOfResults": 100,
                "overrideSearchType": "HYBRID"   
            }
        },
        "retrievalQuery": {
            "text": query
        }
    }
    
    # Retrieve from knowledge base
    return runtime.retrieve(**kwargs)


@Tools.tool("retrieve", "data")
def get_article(search_term):
    """_
    Function to retrieve data from wiki page
    """
    
    results = wikipedia.search(search_term)
    
    if not results:
        return "Can not find any relevant information about that"
    first_result = results[0]
    
    page = wikipedia.page(first_result, auto_suggest=False)
    
    return page.content


@Tools.tool("retrieve", "data")
def get_information(search_term: str) -> str:
    """
    Use this tool to search for. Use this tool when the users asks for general news.
    
    @param search_term: Query search tool
    """
    search = DuckDuckGoSearchRun(max_results = 5)
    result = search.run(search_term)
    return result