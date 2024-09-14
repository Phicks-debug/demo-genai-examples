import boto3

from modules.models import Claude
from modules.core import Prompts
from toolsdata import return_tool
from termcolor import cprint


system_prompt = """
    If answering the question requires data you were not trained on, you can use the get_article tool to get the contents of a recent wikipedia article about the topic.
    If answering the question related to stocks, you muse use all posible stock tools to get the content, background of that stocks and other related stocks 
    You can search for background information by using get_article, get_vnexpress_news, get_relevant_news tool for background and related content for more indetail information.
    If you can answer the question without needing to get more information, please do so. 
    Only call the tool when needed. 
    Answers should always include detail facts, reference from sources, numbers, clear examples.
    All answers and thinking are in vietnamese.
    Try to request all the tools at the same time in sequence order.
    """


if __name__ == "__main__":
    
    # Create session
    session = boto3.Session()
    
    # Create runtime service
    claudeModel = Claude("3.5-sonnet", "us-east-1", 10, session)
    claudePrompt = Prompts(claudeModel)
    
    # Add tool for the model to use
    claudeModel.tool_add(return_tool())
    
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
            
            result = claudeModel.invoke(system_prompt, streaming=True)
            response = claudeModel.response(result)

            if response["stop_reason"] == "end_turn":
                
                claudeModel.add_to_memory("assistant", response["response"])
                break
            
            elif response["stop_reason"] == "tool_use":
                
                claudeModel.add_tool_to_memory(response["body"])
                tool_results = claudeModel.tool_use(response["tool"])
                claudeModel.add_tool_result_to_memory(tool_results)
            
            cprint(claudeModel.memory.messages, "light_magenta")
        