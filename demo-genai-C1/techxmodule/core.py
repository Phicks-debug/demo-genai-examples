from techxmodule import utils


class Guardrail:
    
    def __init__(self, session) -> None:
        self.session = session
    
    def validate(self, user_input: str) -> bool:
        # Implement your input validation logic here
        # Return True if the input is valid, False otherwise
        return len(user_input.strip()) > 0


class Prompts:
    
    def __init__(self, model: any = None) -> None:
        """
        Initializes the Prompts class with an optional model.

        @param model: An optional model object. If provided, it should have a `name` attribute.
                      If no model is provided, `_prompt_type` is set to "None".

        @raises ValueError: If a model is provided but lacks a `name` attribute.
        """
        self.__model = model if model and hasattr(model, "name") else None
        if not self.__model:
            self.__prompt_type = "None"
        else:
            self.__prompt_type = model.name


    def build(self, user_prompt: str, context_prompt: str = "", example_prompt: str = "", chain_of_thought_prompt: str = None) -> str:
        """
        Builds the final prompt based on the specified model type.

        @param user_prompt: The main user input prompt.
        @param context_prompt: Optional context information (default is empty string).
        @param example_prompt: Optional example prompts (default is empty string).
        @param chain_of_thought_prompt: Optional Chain of Thought prompt (default is None).

        @return: A combined prompt as a single string.
        """
        build_prompt_fn = {
            "claude": self.__build_claude_prompt,
            "llama": self.__build_llama_prompt,
            "mistiAi": self.__build_misti_ai_prompt
        }.get(self.__prompt_type, self.__build_default_prompt)

        return build_prompt_fn(user_prompt, context_prompt, example_prompt, chain_of_thought_prompt)


    def __build_claude_prompt(self, user_prompt: str, context_prompt: str = "", example_prompt: str = "", chain_of_thought_prompt: str = None) -> str:
        """
        Builds a prompt specifically for the Claude model using the utility functions from the model.

        @return: Combined and sanitized prompt for Claude.
        """
        return self.__build_prompt_with_utils(user_prompt, context_prompt, example_prompt, chain_of_thought_prompt)

    
    def __build_llama_prompt(self, user_prompt: str, context_prompt: str = "", example_prompt: str = "", chain_of_thought_prompt: str = None) -> str:
        pass
    
    
    def __build_misti_ai_prompt(self, user_prompt: str, context_prompt: str = "", example_prompt: str = "", chain_of_thought_prompt: str = None) -> str:
        pass
    

    def __build_default_prompt(self, user_prompt: str, context_prompt: str = "", example_prompt: str = "", chain_of_thought_prompt: str = None) -> str:
        """
        Builds a default prompt with no specific model optimizations.

        @return: Combined and sanitized default prompt.
        """
        return self.__build_prompt_without_utils(user_prompt, context_prompt, example_prompt, chain_of_thought_prompt)


    def __build_prompt_with_utils(self, user_prompt: str, context_prompt: str, example_prompt: str, chain_of_thought_prompt: str) -> str:
        """
        Helper method to build prompts using model utility methods for models like Claude.

        @return: A combined and sanitized prompt string.
        """
        prompt = utils.combine_string([
            self.__model.build_context_prompt(context_prompt),
            self.__model.build_user_prompt(user_prompt),
            self.__model.build_cot_prompt(chain_of_thought_prompt),
            self.__model.build_example_prompt(example_prompt)
        ])
        return utils.sanitize_input(prompt)


    def __build_prompt_without_utils(self, user_prompt: str, context_prompt: str, example_prompt: str, chain_of_thought_prompt: str) -> str:
        """
        Helper method to build prompts without using any model-specific utilities.

        @return: A combined and sanitized prompt string.
        """
        prompt = utils.combine_string([context_prompt, user_prompt, chain_of_thought_prompt, example_prompt])
        return utils.sanitize_input(prompt)


class Tools:
    """
    A utility class designed to manage and apply decorators to functions interacting with specific tools.

    This class provides a decorator generator to wrap functions with additional metadata 
    about the tool's action and data type.
    """

    def __init__(self) -> None:
        """
        Initializes the Tools class. Currently serves as a placeholder.
        """
        pass

    @staticmethod
    def tool(action: str, data_type: str):
        """
        Decorator generator that adds metadata to the result of the decorated function.

        @param action: The action the tool performs (e.g., "fetch_data").
        @param data_type: The type of data the tool returns (e.g., "text").

        @return: A decorator function that wraps the original function, adding metadata to its output.
        """
        def tool_decorator(func):
            def wrapper(*args, **kwargs):
                try:
                    result = func(*args, **kwargs)
                    return {
                        "text": result,
                        "type": data_type,
                        "action": action
                    }
                except (TypeError, KeyError) as e:
                    return {
                        "error": f"Error using tool: {e}",
                        "type": "parameterError",
                        "action": action
                    }
            return wrapper
        return tool_decorator
