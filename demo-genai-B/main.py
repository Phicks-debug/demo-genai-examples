import utils, boto3


if __name__ == "__main__":
    
    # Create session
    session = boto3.Session(region_name="us-east-1")
    
    # Create runtime service
    bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-east-1")
    bedrock_agent_runtime = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    
    while True:

        # Input user prompt and declare system prompt for instruction
        usr_prompt = input("user: ")
        
        # Exit app conditions
        if usr_prompt == "exit()":
            break
        
        sys_prompt = "Answer in vietnamese only"
        
        # Compress into API POST request to send to knowledge base
        kb_kwargs = {
            "knowledgeBaseId": "AYP6WXNCZ0",
            "retrievalConfiguration": {
                "vectorSearchConfiguration": {
                    "numberOfResults": 15,
                    "overrideSearchType": "HYBRID"   
                }
            },
            "retrievalQuery": {
                "text": usr_prompt
            }
        }
        
        # Retrieve from knowledge base
        retrieve_response = bedrock_agent_runtime.retrieve(**kb_kwargs)
        
        #Parser the retrived response into context prompt
        ctx_prompt = utils.build_context_prompt(retrieve_response)
        
        # Format user prompt and add instructions (CoT technique)
        usr_prompt = utils.build_user_prompt(usr_prompt)
        cot_prompt = utils.build_cot_prompt()
        
        # Add examples (Multishot technique)
        exmaples = utils.read_txt_file("data/example_answers.txt")
        exm_prompt = utils.build_example_prompt(exmaples)

        # Build in payload with inference parameters
        payload = utils.build_payload(usr_prompt, sys_prompt, ctx_prompt, cot_prompt)

        # Compress into API POST request to send to amazon bedrock service
        kwargs = {
            "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
            "accept": "application/json",
            "contentType": "application/json",
            "body": payload
        }

        # # Without streaming
        # response = bedrock_runtime.invoke_model(**kwargs)
        # utils.extract_response(response, debug=True)
        
        # With streaming
        # Get the response back from the model
        response = bedrock_runtime.invoke_model_with_response_stream(**kwargs)
        
        # Stream the response into console
        utils.stream_response(response)