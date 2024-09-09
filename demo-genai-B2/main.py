import boto3

from modules.models import Claude
from modules.core import Prompts


functionA = {
    "name": "get_time_date",
    "description": "Tool for knowing the current time and day and year, month now at the moment. \
        Use this to know only the time at the moment. Do not provide any input schema (no parameter for this function).",
    "input_schema": {
        "type": "object",
    }
}


functionB = {
    "name": "link_to_knowledgebase",
    "description": "A datasource that store every things about Chí Phèo story by Nam Cao. Use this to search more about the story,\
        the characters name Bá Kiến, Thị Nở, Tự Lãng, Chí Phèo, or other small characters in the story. \
            Use this to know more and to analysis when asking about the story and the characters.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "The texts or keywords that you want to search for the reference  or for more information about it. \
                    This should be a pargraphs, a lot of string that you want to find more context,or a text that can help \
                        you understand more about the story, the characters "
            }
        },
        "required": ["query"]
    }
}


functionC = {
    "name": "get_article",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_stock_price = {
    "name": "get_stock_price",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_stock_intraday = {
    "name": "get_stock_intraday",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_info = {
    "name": "get_company_info",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_events = {
    "name": "get_company_events",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_shareholders = {
    "name": "get_company_shareholders",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_inside_trades = {
    "name": "get_company_inside_trades",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_subsidiaries = {
    "name": "get_subsidiaries",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_dividends = {
    "name": "get_dividends",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_balance_sheet = {
    "name": "get_company_balance_sheet",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_income_statement = {
    "name": "get_company_income_statement",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_cash_flow = {
    "name": "get_cash_flow",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_company_financial_ratio = {
    "name": "get_company_financial_ratio",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_vnexpress_news = {
    "name": "get_vnexpress_news",
    "description": "A tool to retrieve an up to date Wikipedia article.",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a wikipedia article by title"
            },
        },
        "required": ["search_term"]
    }
}


tool_get_relevant_news = {
    "name": "get_relevant_news",
    "description": "Use this tool to search for general news. Use this tool when the users asks for general news, that is recently.\
                    Can use this tool to search news about stock only IF ALL THE OTHER TOOLS DID NOT RETURN any\
                    relavant answers or did not return any related articles",
    "input_schema": {
        "type": "object",
        "properties": {
            "search_term": {
                "type": "string",
                "description": "The search term to find a news about that article by title"
            },
        },
        "required": ["search_term"]
    }
}


system_prompt = """
    You will be asked a question by the user. 
    If answering the question requires data you were not trained on, you can use the get_article tool to get the contents of a recent wikipedia article about the topic. 
    If you can answer the question without needing to get more information, please do so. 
    Only call the tool when needed. 
    All answers and thinking are in vietnamese.
    """


if __name__ == "__main__":
    
    # Create session
    session = boto3.Session()
    
    # Create runtime service
    claudeModel = Claude("3-haiku", "us-east-1", 10, session)
    claudePrompt = Prompts(claudeModel)
    
    # Add tool for the model to use
    claudeModel.tool_add([functionA, functionB, functionC, tool_get_relevant_news])
    
    # Main loop for application
    while True:
        
        # Input user prompt and declare system prompt for instruction
        userPrompt = input("user: ")
        
        # Exit app conditions
        if userPrompt == "exit()":
            break
        
        prompt = claudePrompt.build(userPrompt)
        
        claudeModel.add_to_memory("user", prompt) 
        
        # Sub-loop for tool use
        while True: 

            result = claudeModel.invoke(system_prompt, streaming=False)
            
            response = claudeModel.response(result)          
            # response = claudeModel.stream_response(result)

            if response["stop_reason"] == "end_turn":
                
                claudeModel.add_to_memory("assistant", response["response"])
                break
            
            elif response["stop_reason"] == "tool_use":
                
                claudeModel.add_tool_to_memory(response["body"])
                tool_result = claudeModel.tool_use(response["tool"])
                claudeModel.add_tool_result_to_memory(response["tool"]["id"], tool_result) 

        