# A real API response payload stored in variable

api_response = { # master dictionary
    "id": "chatcmpl-9A8B7C",
    "object": "chat.completion",
    "created": 1713524800,
    "model": "gpt-4o-mini",
    "choices":[
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content" : "A vector database stores data as numerical vectors, allowing fast similarity searches based on context rather than exact keyword matches."
            },
            "finish_reason":"stop"
        }
    ],
    "usage":{
        "prompt_tokens": 15,
        "completion_tokens": 24,
        "total_tokens": 39
    }
}

tokens_used = api_response["usage"]["total_tokens"] #accessing the keys from master dictionary 
print(f"Tokens consumed: {tokens_used}")

