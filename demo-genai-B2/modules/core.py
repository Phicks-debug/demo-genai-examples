from modules import utils


class Prompts:
    
    def __init__(self, model: any = None) -> None:
        """
        Initializes the class with an optional model.

        @param model: An optional model object. If provided, it should have a `name` attribute. If no model is provided, the default is to set `_prompt_type` to "None".

        @raises ValueError: If a model is provided but does not have a `name` attribute

        @return: None
        """
        
        if not model:
            self._prompt_type = "None"
            return 
        
        if hasattr(model, "name"):
            self._model = model
        else:
            ValueError(" Invalid model type was passed in")
        
    
    def build(self, user_prompt, context_prompt:any="", 
              example_prompt="", chainOfThough_prompt:str|None=None):
        """       
        Build prompt.
        
        @param user_prompt: A string containing the main user prompt.
        @param context_prompt: A string containing the context prompt (default is an empty string).
        @param example_prompt: A string containing example prompts (default is an empty string).
        @param chainOfThough_prompt: A string containing chain-of-thought prompts (default is None).
        
        @return engineered prompt
        """
            
        # Select the desirer prompt engineering tool
        if self._model.name == "claude":
            new_prompt = self._buildClaudePrompt(user_prompt, context_prompt, 
                                           example_prompt, chainOfThough_prompt)
        elif self._model.name == "llama":
            new_prompt =  self._buildLlamaPrompt(user_prompt, context_prompt, 
                                          example_prompt, chainOfThough_prompt)
        elif self._model.name == "mistiAi":
            new_prompt =  self._buildMistiAiPrompt(user_prompt, context_prompt, 
                                            example_prompt, chainOfThough_prompt)
        else:
            return self._buildDefaultPrompt(user_prompt, context_prompt, 
                                            example_prompt, chainOfThough_prompt)
        
        return new_prompt

    
    def _buildClaudePrompt(self, user_prompt, context_prompt:any="", 
                           example_prompt="", chainOfThough_prompt:str|None=None):
        """
        Prompt engineering method restrictly for Anthropic Claude Model
        """
        
        prompt = utils.combine_string(
            [
                self._model._build_context_prompt(context_prompt),
                self._model._build_user_prompt(user_prompt), 
                self._model._build_cot_prompt(chainOfThough_prompt),
                self._model._build_example_prompt(example_prompt)
            ]
        )
        
        return utils.sanitize_input(prompt)
    
    
    def _buildDefaultPrompt(self, user_prompt, context_prompt:any="", 
                           example_prompt="", chainOfThough_prompt:str|None=None):
        """
        Default prompt engineering
        
        ***
        """
        prompt = utils.combine_string(
            [
                context_prompt, user_prompt, chainOfThough_prompt, example_prompt
            ]
        )
        
        return utils.sanitize_input(prompt)
    

class Tools:
    """
    A utility class designed to manage and apply decorators to functions that interact with specific tools.

    This class provides a decorator generator method that wraps functions with additional metadata about 
    the tool's action and data type, making it easier to standardize outputs for various tool operations.

    Methods
    -------
    __init__() -> None:
        Initializes the Tools class. Currently, it does not take any arguments and serves as a placeholder.

    tool(action: str, data_type: str):
        A decorator generator that adds metadata to the result of the decorated function. This metadata 
        includes the type of data returned by the tool and the specific action the tool performs.

        Parameters
        ----------
        action : str
            A string representing the action the tool performs (e.g., "fetch_data", "analyze_text").
        data_type : str
            A string representing the type of data the tool returns (e.g., "text", "image").

        Returns
        -------
        tool_decorator : function
            A decorator function that wraps the original function, adding metadata to its output.

        Example Usage
        -------------
        @Tools.tool(action="fetch_data", data_type="text")
        def my_tool_function(param1, param2):
            return "This is the result of the tool operation."
        
        # This would return:
        # {
        #     "text": "This is the result of the tool operation.",
        #     "type": "text",
        #     "action": "fetch_data"
        # }
    """

    def __init__(self) -> None:
        pass

    def tool(action: str, data_type: str):
        def tool_decorator(func):
            def wrapper(*args, **kwargs):
                result = func(*args, **kwargs)
                
                return {
                    "text": result,
                    "type": data_type,
                    "action": action
                }
                
            return wrapper
        return tool_decorator