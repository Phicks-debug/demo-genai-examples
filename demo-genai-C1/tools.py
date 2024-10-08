from techxmodule.core import Tools

import boto3, json
import wikipedia # type: ignore

import requests
from langchain_community.tools import DuckDuckGoSearchRun # type: ignore

import urllib.parse


@Tools.tool("retrieve", "data")
def call_wolframalpha(query: str) -> str:
    """
    Function to call wolframalpha API
    """
    
    encoded_query = urllib.parse.quote(query)
    
    url = f"https://www.wolframalpha.com/api/v1/llm-api?input={encoded_query}s&appid=AQHXEG-WE9WU4T6K6"
    
    return requests.get(url).text


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

