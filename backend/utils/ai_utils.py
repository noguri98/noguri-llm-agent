import ollama

def ollama_inference(prompt: str, model: str = "qwen3:8b") -> str:
    response = ollama.chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])
    return response['message']['content']
