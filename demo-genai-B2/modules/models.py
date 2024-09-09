import json, tools
from modules import utils
from modules.messages import ChatMessage, Image
import xml.etree.ElementTree as ET


class LLM():
    """
    Parent LLM class
    """
    
    def __init__(self, name: str, max_chat_memmory: int, session, region_name: str) -> None:
        self.name = name
        self.recent_response = ""
        self.memory = ChatMessage(max_chat_message=max_chat_memmory+4)  # Add buffer, DO NOT REMOVE
        self.runtime = session.client("bedrock-runtime", region_name=region_name)
        self.tools = []
    
    
    def assess_memory(func):
        """
        Decorator to assess memory before adding a new message.
        If memory exceeds the set limit, purifies the recent question and removes old messages.
        """
        def wrapper(self, *args, **kwargs):
            # if len(self.memory.messages) >= 2:
            #     self.memory._purify_recent_question()

            func(self, *args, **kwargs)

            if len(self.memory.messages) > self.memory.max_chat_message + 1:
                
                # Initiate delete the first message
                self.memory.messages.pop(0)
                
                # Remove the oldest message chat until the memory start with use or 
                # not start with the tool result message
                while self.memory.messages[0]["role"] != "user" or \
                    self.memory.messages[0]["content"][0]["type"] == "tool_result":
                    
                    self.memory.messages.pop(0)

        return wrapper
    

    @assess_memory
    def add_to_memory(self, role: str, text: str, images: list[Image] | None = None) -> None:
        """
        Adds a new message to the memory. The `assess_memory` decorator is 
        applied to this method to manage memory, ensuring that older messages are pruned if the 
        memory exceeds its predefined limit.

        @param role: The role of the sender of the message. This should be either "user" or "assistant".
        @param text: The content of the message to be added to memory.
        @param images: Optional list of images associated with the message. 
                    Defaults to None.

        @return: None
        """
        
        self.memory.append_message(role, text, images)
            
    
    @assess_memory
    def add_tool_result_to_memory(self, tool_use_id, content) -> None:
        """
        Adds tool result to the memory. The `assess_memory` decorator is 
        applied to this method to manage memory, ensuring that older messages are pruned if the 
        memory exceeds its predefined limit.

        @param tool_use_id: An id of the tool that the model request to use.
        @param content: The content of the result to be added to memory.
        @param images: Optional list of images associated with the message. 
                    Defaults to None.

        @return: None
        """
        
        # Need to fix so that I could add picture to it
        self.memory.append_tool_result(tool_use_id, content)
            
    
    @assess_memory
    def add_tool_to_memory(self, tool_content) -> None:
        """
        Adds tool-related content to the chat memory, ensuring memory constraints are respected.

        This method appends tool-specific content to the chat memory. The `assess_memory` decorator is 
        applied to this method to manage memory, ensuring that older messages are pruned if the 
        memory exceeds its predefined limit.

        @param tool_content: The content related to a tool that should be added to the memory. 
                            This could include information such as tool names, parameters, or 
                            results, depending on how the tool content is structured.
        
        @return
        """
        
        self.memory.append_tool(tool_content)
    
    
    def stream_response(self, invoke_result, debug: bool=False) -> any:
        """
        Stream and print model output from an HTTP response in real-time. 
        Optionally print debugging information.

        @param invoke_result: The HTTP response object containing the streamed JSON data.
        @param debug: Boolean flag to print additional debugging information. Defaults to False.
        
        @return: full stream response contain texts and images depend on the response
        
        """
        """
        Đừng cố hiểu code logic cái này làm gì, nó ảo lắm, mất mẹ 2 tiếng cuộc đời em mà vẫn đ hiểu gì.
        Chỉ cần biết là nó trả về câu trả lời full sau khi stream xong. 
        Về sau sẽ add them feature dừng stream, Interupted by user.
        """
        
        full_response = ""

        for event in invoke_result.get("body"):
            chunk = json.loads(event["chunk"]["bytes"])

            # For debugging only
            if chunk['type'] == 'message_delta':
                
                if not debug:
                    print("\n")     # Add spacing for readability
                    break
                
                print(f"\nStop reason: {chunk['delta']['stop_reason']}")
                print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
                print(f"Output tokens: {chunk['usage']['output_tokens']}")

            if chunk['type'] == 'content_block_delta':
                if chunk['delta']['type'] == 'text_delta':
                    text_chunk = chunk['delta']['text']
                    print(text_chunk, end="")
                    
                    # Add stream chunk to the final response.
                    full_response += text_chunk
        
        return {
            "response": full_response,
            "tool": tool,
            "stop_reason": body['stop_reason']
        }
            
    
    def tool_add(self, tool_list: list):
        """
        Add tool for the model to extend its capability
        
        @param tool_list: list of usable tools for the model
        """
        self.tools.extend(tool_list)
        

    def response(self, invoke_result, debug: bool=False) -> any:
        """
        Process and extract the content from a JSON response, optionally printing debugging information.

        This method parses the JSON content from an HTTP response, extracting text and tool usage data. 
        The text is accumulated into a single string, and any tool usage information is captured in a dictionary. 
        If the `debug` flag is set to `True`, additional details about the response are printed, 
        such as the stop reason, stop sequence, and token usage.

        @param invoke_result: The HTTP response object containing the JSON data to be processed. 
        This is expected to have a `body` that can be read and parsed as JSON.
        @param debug: A boolean flag that, when set to `True`, prints additional debugging information 
                    about the response, including stop reason, stop sequence, and token usage. 
                    Defaults to `False`.
            
        @return: A dictionary containing:
        - "response": A string with the concatenated text from the JSON content.
        - "tool": A dictionary with tool usage information, containing:
            - "name": The name of the tool used.
            - "params": The parameters passed to the tool.
        
        If no tool is used, "tool" will be `None`.
        """
        
        full_response = ""
        tool = None
        
        body = json.loads(invoke_result.get("body").read())
        for content_block in body["content"]:
            
            # Check if it is text
            if content_block["type"] == "text":
                print(content_block["text"])
                full_response += content_block["text"]
                
            # Check if it request tool use
            if content_block["type"] == "tool_use":
                tool = {
                    "id": content_block["id"],
                    "name" : content_block["name"],
                    "params": content_block["input"]
                }  

        if debug:
            print(f"\nStop reason: {body['stop_reason']}")
            print(f"Stop sequence: {body['stop_sequence']}")
            print(f"Output tokens: {body['usage']['output_tokens']}")
        
        return {
            "response": full_response,
            "tool": tool,
            "stop_reason": body['stop_reason'],
            "body": body['content']
        }
            
            
    def _assess_messages(self, messages: list|None):
        """
        Assess message and decide to use internal memory or outer memory.
        """
        if (not messages):
            if (len(self.memory.messages) < 0):
                raise AssertionError("Found None in model's memory. \
                    Missing messages from the user, please provide messages")
        
        else:
            self.add_to_memory("user", messages)
        
        return self.memory.messages


class Claude(LLM):
    """
    Anthropic Claude class model
    """
    
    def __init__(self, name: str, region_name: str, max_chat_memmory: int, session) -> None:
        """
        Initializes a new instance of the class with a specific Claude model.
        
        @param name: The name of the Claude model to use. Must be one of "3-haiku", "3-sonnet", "3-opus", or "3.5-sonnet".
        @param region_name: The name of the region that you run the AWS service
        @param max_chat_memmory: The maximum number of previous chat that the model can remember + buffer(4). 
                                2 means 1 for "user", 1 for "assistant"
        @param session: An instance of the boto3 Session object used to create a client 
                        for the Bedrock runtime service.

        @return: None
        """
    
        super().__init__("claude", max_chat_memmory, session, region_name)
        
        if name == "3-haiku":
            self.modelId = "anthropic.claude-3-haiku-20240307-v1:0"
        elif name == "3-sonnet":
            self.modelId = "anthropic.claude-3-sonnet-20240229-v1:0"
        elif name == "3-opus":
            self.modelId = "anthropic.claude-3-opus-20240229-v1:0"
        elif name == "3.5-sonnet":
            self.modelId = "anthropic.claude-3-5-sonnet-20240620-v1:0"
        else:
            raise ValueError(f"modelId is not valid, model name {name} is not found")
    
    
    def invoke(self, system_prompt: str="", messages: list|None = None, 
               temp: float=0.15, top_p: float=0.8, top_k: int=50, streaming: bool|None=True) -> json: 
        """
        Invokes a model with the provided system_prompts and messages, sending a request to the Amazon Bedrock service return the response
        from the model.

        Constructs a payload based on the given parameters and sends it to the API. The method can either stream the response 
        or wait for the entire response to be returned, depending on the `streaming` flag.

        @param system_prompt: A string specifying the characteristic or role name feature to be used by the model.
        @param messages: A list containing the prompts or images to be sent to the model. If None provided, it will trying to use messages from its memory (default is None)
        @param temp: A float specifying the temperature for sampling, which controls the randomness of the output (default is 0.2).
        @param top_p: A float specifying the cumulative probability for nucleus sampling, determining the diversity of the output (default is 0.8).
        @param top_k: An integer specifying the number of top tokens to consider for sampling, influencing the output generation (default is 50).
        @param streaming: A boolean indicating whether to stream the response or wait for the entire response (default is True).

        @return: The response from the Amazon Bedrock service in JSON format, which may vary depending on whether streaming is enabled or not.
        """
        
        assessed_messages = self._assess_messages(messages)
    
        # Build payload based on Claude API
        payload = self._build_payload(system_prompt, assessed_messages, temp, top_p, top_k)
        
        # Compress into API POST request to send to amazon bedrock service
        kwargs = {
            "modelId": self.modelId,
            "accept": "application/json",
            "contentType": "application/json",
            "body": payload
        }
        
        if streaming == True:
            response = self.runtime.invoke_model_with_response_stream(**kwargs)
        else:
            response = self.runtime.invoke_model(**kwargs)
            
        return response       
    
    
    def tool_use(self, tool: dict):
        """
        Executes a tool function based on the provided tool name and parameters.

        This method dynamically invokes a function from the `tools` module using the name specified in 
        the `tool` dictionary. The function is called with the parameters provided in the `tool` dictionary.
        Depending on the type of result returned, the method processes the output accordingly:
        
        - If the result is of type "knowledge_base", it processes the text using a context-building method.
        - If the result is of type "data", it simply returns the text data.
        - If the result is of type "image", it prepares for image-related logic (currently a placeholder).
        
        @param tool: A dictionary containing:
        - "name": The name of the tool function to invoke.
        - "params": A dictionary of parameters to pass to the tool function.
        
        @return: The processed result from the invoked tool, which may be a context-built prompt or text data.
        """
        
        print("Analyzing...")

        # Dynamically invoke the tool function using the tool's name and parameters
        tool_function = getattr(tools, tool["name"])
        result = tool_function(**tool["params"])

        # Handle and proccess result based on its type
        if result["type"] == "documents":
            x = self._build_context_kb_prompt(result["text"])
            print("Analyzing data source from knowledge base...")
            return x

        elif result["type"] == "data":
            print("Getting data from sources...")
            return result["text"]

        elif result["type"] == "image":
            # Placeholder for future logic to handle image results
            print("Image processing not yet implemented.")
            pass
    
        
    def _build_context_kb_prompt(self, 
                    retrieved_json_file, min_relevant_percentage: float = 0.5, debug=False):
        """
        Build a structured long context prompt in XML format from a retrieved JSON file.

        This function processes the retrieved JSON data, filters out irrelevant content based on a 
        minimum relevance score, and constructs an XML document following the guidelines provided 
        by Anthropic for long-context prompts.

        @param retrieved_json_file: The JSON object containing retrieval results and metadata.
        @param min_relevant_percentage: The minimum relevance score required for a context block to be included. Defaults to 0.5.
        @param debug: Boolean flag to print the XML structure for debugging purposes. Defaults to False.
        
        @return: A string representing the XML structure of the context prompt.
        """
        
        if retrieved_json_file == "":
            return ""
        
        # Start creating structure context block
        # Follow the GUIDELINE from 
        # https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/long-context-tips#example-multi-document-structure
        documents = ET.Element("documents")
        
        if retrieved_json_file["ResponseMetadata"]["HTTPStatusCode"] != 200:
            documents.text = "Error in getting data source from knowledge base. No context is provided"
        else:
            body = retrieved_json_file["retrievalResults"]
            
            # Iterate through body retrieve each into document
            # Example to add multiple document elements with an incrementing index attribute
            for i, context_block in enumerate(body):
                
                # Filter irrelevant knowledge
                if context_block["score"] < min_relevant_percentage:
                    break
                
                # Create XML tag follow the Claude guideline above
                document = ET.SubElement(documents, "document", {"index": str(i + 1)})
                source = ET.SubElement(document, "source")
                content = ET.SubElement(document, "document_content")
                
                # Add source and content to assigned XML tag
                source.text = utils.iterate_through_location(context_block["location"])
                content.text = context_block["content"]["text"]
            
            # For debug only
            if debug:
                ET.dump(documents)
        
        return ET.tostring(documents, encoding="unicode", method="xml")
    
    
    def _build_context_prompt(self, prompt: str):
        
        if prompt == "":
            return ""
        
        cot_prompt = ET.Element("context")
        cot_prompt.text = prompt
        return ET.tostring(cot_prompt, encoding="unicode", method="xml")

    
    def _build_cot_prompt(self, prompt: str|None = None):
        """
        Constructs an XML representation of a Chain of Thought (CoT) prompt.

        If a prompt is provided, it is used as the content of an XML element with the tag "instruction".
        If no prompt is provided, a default template is used to guide the Chain of Thought process.

        @param prompt: An optional string containing the prompt text to be included in the XML. 
                    If None, a default template prompt is used.

        @return: A string containing the XML representation of the Chain of Thought prompt.
        """
        
        if prompt == None:
            # Generate a default template prompt if not provided
            # Can use this for template for your own Chain of Thought prompt
            prompt = "\
                Analyze which actions need to do after reading from the <request> tag. \
                Think step-by-step what to do in <thinking> tag. \
                Finally give an answer or solve the request in <answer> tag. \
                Follow the answer format in <exmaple> tag if included \
                else feel free to use your format. \
            "
        
        cot_prompt = ET.Element("instruction")
        cot_prompt.text = prompt
        return ET.tostring(cot_prompt, encoding="unicode", method="xml")


    def _build_example_prompt(self, prompt: str):
        """
        Constructs an XML representation of an example prompt.

        This function creates an XML element with the tag "example" and sets its text content
        to the provided prompt. The resulting XML is then returned as a Unicode string.

        @param prompt: A string containing the prompt text to be included in the XML.

        @return: A string containing the XML representation of the example prompt.
        """
        
        if prompt == "":
            return ""
        
        example_prompt = ET.Element("example")
        example_prompt.text = prompt
        return ET.tostring(example_prompt, encoding="unicode", method="xml")
    
    
    def _build_payload(self, sys_prompt, messages, temp, p, k) -> json:
        """
        Constructs a JSON payload for an API request 
        based on the provided prompts and parameters.
        
        """
        
        return json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4000, # Recommend
            "system": sys_prompt,
            "messages": messages,
            "tools": self.tools,
            # "tool_choice": {},        # Should try "auto", "any", "tool".
            "temperature": temp,
            "top_p": p, "top_k": k,
            "stop_sequences": []
        })


    def _build_user_prompt(self, prompt: str):
        """
        Constructs an XML representation of a user prompt.

        This function creates an XML element with the tag "request" and sets its text content
        to the provided prompt. The resulting XML is then returned as a Unicode string.

        @param prompt: A string containing the prompt text to be included in the XML.

        @return: A string containing the XML representation of the user prompt.
        """
        
        user_prompt = ET.Element("request")
        user_prompt.text = prompt
        return ET.tostring(user_prompt, encoding="unicode", method="xml")
