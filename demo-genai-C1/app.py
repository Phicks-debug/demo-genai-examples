import boto3
import json

from techxmodule.core import Guardrail, Prompt
from techxmodule.agents import Agent
from techxmodule.events import EventBus
from techxmodule.models import Claude

REGION = "us-east-1"


class LLMApplication:
        
    def __init__(self) -> None:
        self.event_bus = EventBus()
        self.session = boto3.Session(region_name=REGION)
        
        self.llm = Claude("3.5-sonnet", REGION, 10, self.session)
        self.prompt = Prompt()
        
        self.guardrail = Guardrail()

        
    def run(self):
        while True:
            user_input = input("Enter your prompt (or 'quit' to exit): ")
            if user_input.lower() == "quit":
                break
            self.handle_input_guardrail(user_input)
    
    def handle_input_guardrail(self, user_input: str):
        if self.guardrail.validate(user_input):
            self.event_bus.publish("JudgeEvent", user_input)
        else:
            print("Invaid input. Please try again")
    
    async def judge_prompt(self, user_prompt: str):
        if self.judging_agent.judge_prompt(user_prompt):
            self.event_bus.publish("GoodQueryEvent", user_prompt)
        else:
            self.event_bus.publish("BadQueryEvent", user_prompt)
            
    async def handle_reprompt(self, prompt: str):
        new_prompt = self.prompt_processing.reprompt(prompt)
        self.event_bus.publish("JudgeEvent", new_prompt)
        
    async def handle_chat_history(self, messasge: str):
        pass
        
        
if __name__ == "__main__":
    app = LLMApplication()
    app.run()