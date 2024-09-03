import boto3
import json

import xml.etree.ElementTree as ET


def create_services(
    service_name: str = "bedrock-runtime", 
    session: bool=False
):
    """
    Create a Boto3 client for a specified AWS service.

    @param service_name: The name of the AWS service to create a client for. Defaults to "bedrock-runtime".
    @param session: Boolean flag indicating whether to create a new session. Defaults to False.
    
    @return: A Boto3 client for the specified service.
    """
    
    # Create Session for user
    if session:
        ss = boto3.Session(
            region_name = "us-east-1"
        )

    # Select services
    return ss.client(
        service_name = service_name,
    )


def extract_response(response, debug: bool=False):
    """
    Extract and print the content of a JSON response. Optionally print debugging information.

    @param response: The HTTP response object containing the JSON data.
    @param debug: Boolean flag to print additional debugging information. Defaults to False.
    
    @return: None
    """
    
    body = json.loads(response.get('body').read())
    for con_block in body["content"]:
        print(con_block["text"])

    if debug:
        print(f"\nStop reason: {body['stop_reason']}")
        print(f"Stop sequence: {body['stop_sequence']}")
        print(f"Output tokens: {body['usage']['output_tokens']}")


def stream_response(response, debug: bool=False):
    """
    Stream and print content from an HTTP response in real-time. Optionally print debugging information.

    @param response: The HTTP response object containing the streamed JSON data.
    @param debug: Boolean flag to print additional debugging information. Defaults to False.
    
    @return: None
    """
    
    for event in response.get("body"):
        chunk = json.loads(event["chunk"]["bytes"])

        # For debugging only
        if chunk['type'] == 'message_delta':
            
            if not debug:
                print()     # Add spacing for readability
                return
            
            print(f"\nStop reason: {chunk['delta']['stop_reason']}")
            print(f"Stop sequence: {chunk['delta']['stop_sequence']}")
            print(f"Output tokens: {chunk['usage']['output_tokens']}")

        if chunk['type'] == 'content_block_delta':
            if chunk['delta']['type'] == 'text_delta':
                print(chunk['delta']['text'], end="")


def extract_model_tag(json_data, model_tag):
    """
    Extract and return specific model tags from JSON data.

    @param json_data: The JSON data, either as a string or a dictionary, containing model information.
    @param model_tag: The key to extract from each model's summary in the JSON data.
    
    @return: A list of extracted model tags, or 0 if no model_tag is provided.
    """
    
    if not model_tag:
        print(json_data)
        return 0
    
    # Parse the JSON data if it's a string
    if isinstance(json_data, str):
        data = json.loads(json_data)
    else:
        data = json_data
    
    # Initialize a list to store the modelArns
    model_tags = []
    
    # Access the modelSummaries list
    model_summaries = data.get('modelSummaries', [])
    
    # Extract modelArn from each model summary
    for model in model_summaries:
        model_t = model.get(model_tag)
        if model_t:
            model_tags.append(model_t)
    
    return model_tags


def get_all_model(region_name, model_tag: str|None=None, model_name: str|None=None):
    """
    Retrieve and print model information from AWS Bedrock based on model tags and/or model names.

    @param region_name: The AWS region name where the Bedrock service is located.
    @param model_tag: The specific model tag to filter the models by. Defaults to None.
    @param model_name: The specific model name to filter the models by. Defaults to None.
    
    @return: None
    """
    
    bedrock = boto3.client(service_name="bedrock", region_name = region_name)
    for i in extract_model_tag(bedrock.list_foundation_models(), model_tag):
        if model_name and model_name in i:
            print(i)
        elif not model_name :
            print(i)


def build_payload(
    user_prompt: str,
    system_prompt: str="", 
    context_prompt: str="",
    example_prompt: str="",
    chainOfThough_prompt: str="",
    temp: float=0.2, top_p: float=0.7, top_k: int=50):
    """
    Constructs a JSON payload for an API request based on the provided prompts and parameters.

    Combines various prompts into a single string, sanitizes the input, and formats it into a JSON object 
    with additional configuration options for an API call such as 
    inference varaibles, implying [ROLE_NAME], stope sequnce

    @param user_prompt: A string containing the main user prompt.
    @param system_prompt: A string containing the system prompt (default is an empty string).
    @param context_prompt: A string containing the context prompt (default is an empty string).
    @param example_prompt: A string containing example prompts (default is an empty string).
    @param chainOfThough_prompt: A string containing chain-of-thought prompts (default is an empty string).
    @param temp: A float specifying the temperature for sampling (default is 0.2).
    @param top_p: A float specifying the cumulative probability for nucleus sampling (default is 0.7).
    @param top_k: An integer specifying the number of top tokens to consider for sampling (default is 50).

    @return: A JSON string representing the API request payload with combined prompts and configured parameters.
    """

    prompt = combine_string([context_prompt, user_prompt, example_prompt, chainOfThough_prompt])
    prompt = sanitize_input(prompt)
    
    return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000, # Recommend
        "system": system_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": prompt
                    }
                ]
            }
        ],
        "temperature": temp,
        "top_p": 0.7,
        "top_k": 50,
        "stop_sequences": []
    })
    
    
def combine_string(list_of_string: list) -> str:
    """
    Concatenates a list of strings into a single string with newline separators.

    @param list_of_string: A list of strings to be concatenated.
    
    @return: A single string formed by joining the input strings with newline characters.
    """
    
    result = ""
    for s in list_of_string:
        result = result + s + "\n"
    return result
        

def iterate_through_location(location: json):
    """
    Iterates through a dictionary of locations to find the first valid URI or URL.

    The function checks each entry in the dictionary to see if it contains a 'uri' or 'url' key,
    returning the first non-None value found.

    @param location: A dictionary where each value may contain 'uri' or 'url' keys.

    @return: The first non-None URI or URL found in the dictionary, or None if neither is found.
    """
    
    for loc_data in location.values():
            
            if not isinstance(loc_data, dict):  # Check if the location data is a dictionary
                continue
            
            # Check if 'uri' or 'url' key exists in the dictionary
            uri = loc_data.get("uri")
            url = loc_data.get("url")
            
            # Return the first found uri or url
            if uri:
                return uri
            if url:
                return url
    return None


def read_txt_file(file_name: str) -> str:
    """
    Reads the contents of a text file into a string.

    @param file_name: The path to the text file to be read.

    @return: The contents of the file as a string.
    """
    
    with open(file_name, 'r', encoding='utf-8') as file:
    # Read the contents of the file into a string
        file_contents = file.read()
    return file_contents


def sanitize_input(text: str) -> str:
    """
    Remove leading and trailing whitespace
    
    @param text: input text
    
    @return: sanitized text
    """
    
    text = text.strip()
    # Check if the text is not empty
    if not text:
        raise ValueError("Input text cannot be empty or only whitespace.")
    return text
        
        
def build_context_prompt(retrieved_json_file: json, min_relevant_percentage: float = 0.5, debug=False):
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
            source.text = iterate_through_location(context_block["location"])
            content.text = context_block["content"]["text"]
        
        # For debug only
        if debug:
            ET.dump(documents)
    
    return ET.tostring(documents, encoding="unicode", method="xml")


def build_example_prompt(prompt: str):
    """
    Constructs an XML representation of an example prompt.

    This function creates an XML element with the tag "example" and sets its text content
    to the provided prompt. The resulting XML is then returned as a Unicode string.

    @param prompt: A string containing the prompt text to be included in the XML.

    @return: A string containing the XML representation of the example prompt.
    """
    
    example_prompt = ET.Element("example")
    example_prompt.text = prompt
    return ET.tostring(example_prompt, encoding="unicode", method="xml")


def build_user_prompt(prompt: str):
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




def build_cot_prompt(prompt: str|None = None):
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
            Follow the answer format in <exmaple> tag if it has \
            else feel free to use your format. \
        "
    
    cot_prompt = ET.Element("instruction")
    cot_prompt.text = prompt
    return ET.tostring(cot_prompt, encoding="unicode", method="xml")

    