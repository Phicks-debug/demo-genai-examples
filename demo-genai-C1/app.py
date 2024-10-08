import boto3

from termcolor import colored   # type: ignore
from techxmodule.core import Guardrail, Prompts
from techxmodule.events import EventBus
from techxmodule.models.chat import Claude
from techxmodule.models.instruct import LLama
from techxmodule.utils import real_time

USER = "user"
BOT = "assistant"
REGION = "us-east-1"
END_CODE = "/bye"


function_list = [{
        "name": "get_weather",
        "description": "Get weather info for places",
        "parameters": {
            "type": "dict",
            "required": [
                "city"
            ],
            "properties": {
                "city": {
                    "type": "string",
                    "description": "The name of the city to get the weather for"
                },
                "metric": {
                    "type": "string",
                    "description": "The metric for weather. Options are: celsius, fahrenheit",
                    "default": "celsius"
                }
            }
        }
    }]


instruction = f"""You are an introvert shy assistant bot. Today time and Date: {real_time()}"""

        
if __name__ == "__main__":
    session = boto3.Session(region_name=REGION)
    claude = Claude("3-haiku", session, REGION, 10)
    llama = LLama("3.2-3B", session, REGION, 0)
    llama_prompt = Prompts(llama)
    claude_prompt = Prompts(claude)
    
    while True:
        user_input = input("\n\nEnter your prompt (or '/bye' to exit): ")
        if user_input.lower() == END_CODE:
            break
        
        
        llama_formated_prompt = llama_prompt.build(user=user_input, 
                                    instruction=instruction)
        claude_formated_prompt = claude_prompt.build(user=user_input)
        
        
        claude.add_to_memory(USER, claude_formated_prompt)

        print("\nLLama answer: ")
        llama_response = llama.invoke(
            messages=llama_formated_prompt, 
            max_token=512,
            streaming=True)     
        
        print("\n\nClaude answer: ")
        claude_response = claude.invoke(
            system_prompt=instruction, 
            streaming=True
        )
        
        claude.add_to_memory(BOT, claude_response["response"])
        
        
        