import json, utils


def build_payload(user_prompt: str, sys_prompt: str, temp: float):
        return json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 4000, # Recommend
        "system": sys_prompt,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": user_prompt
                    }
                ]
            }   
        ],
        "temperature": temp,
        "top_p": 0.7,
        "top_k": 50,
        "stop_sequences": []
    })


if __name__ == "__main__":
    
    # Create runtime service
    bedrock_runtime = utils.create_services(session=True)
    
    while True:

        # Input user prompt and declare system prompt for instruction
        usr_prompt = input("user: ")
        
        # Exit app conditions
        if usr_prompt == "exit()":
            break
        
        sys_prompt = "response only in vietnamese"

        # Build in payload with inference parameters
        payload = build_payload(usr_prompt, sys_prompt, temp=0.25)

        # Compress into API POST request to send to amazon bedrock service
        kwargs = {
            "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
            "accept": "application/json",
            "contentType": "application/json",
            "body": payload
        }

        # Without streaming
        # response = bedrock.invoke_model(**kwargs)
        # utils.extract_response(response, debug=True)
        
        # With streaming
        # Get the response back from the model
        response = bedrock_runtime.invoke_model_with_response_stream(**kwargs)
        
        # Stream the response into console
        utils.stream_response(response)