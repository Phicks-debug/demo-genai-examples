import boto3
import json


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


def get_all_model(region_name, model_tag: str=None, model_name: str=None):
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
