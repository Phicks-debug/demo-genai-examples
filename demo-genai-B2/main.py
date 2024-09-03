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
    claudeModel.tool_add([functionA, functionB, functionC])
    
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

        