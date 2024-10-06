import boto3, json, pytz

from termcolor import colored   # type: ignore
from techxmodule.core import Guardrail, Prompts
from techxmodule.events import EventBus
from techxmodule.models.chat import Claude
from techxmodule.models.instruct import LLama
from datetime import datetime

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


instruction_prompt = f"""
    You are an expert in composing functions. You are given a question and a set of possible functions.
    
    Cutting Knowledge Date: December 2023
    Today time and Date: {datetime.now(tz = pytz.timezone("Asia/Bangkok")).strftime('%Y-%m-%d %H:%M:%S %Z')}
    
"""


tool_prompt = f"""
    Based on the question, you will need to make one or more function/tool calls to achieve the purpose.
    If none of the function can be used, point it out. If the given question lacks the parameters required by the function,
    also point it out. You should only return the function call in tools call sections.

    If you decide to invoke any of the function(s), you MUST put it in the format of [func_name1(params_name1=params_value1, params_name2=params_value2...), func_name2(params)]
    You SHOULD NOT include any other text in the response.

    Here is a list of functions in JSON format that you can invoke.
    {json.dumps(function_list)}
"""

        
if __name__ == "__main__":
    session = boto3.Session(region_name=REGION)
    claude = Claude("3-haiku", session, REGION, 10)
    llama = LLama("3.2-11B", session, REGION, 0)
    guardrail = Guardrail(session)
    
    while True:
        user_input = input("\n\nEnter your prompt (or '/bye' to exit): ")
        if user_input.lower() == END_CODE:
            break
        
        formatted_prompt = f"""
        <|begin_of_text|><|start_header_id|>system<|end_header_id|>
        
        {instruction_prompt}
        {tool_prompt}
        <|eot_id|><|start_header_id|>user<|end_header_id|>

        {user_input}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
        """

        llama_invoke_result = llama.invoke(
            messages=formatted_prompt, 
            max_token=512, 
            streaming=True)     
        
        # claude_invoke_result = claude.invoke(
        #     messages=user_input, system_prompt="You are an helpful assistant", streaming=True
        # ) 
        
        print("\nLLama answer: ")
        llama.response(llama_invoke_result)
        
        # print("\n\nClaude answer: ")
        # claude.response(claude_invoke_result)