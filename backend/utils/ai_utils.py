import ollama
from . import ai_utils
import database

def ollama_inference(prompt: str, model: str = "qwen3:8b", history: list = None):
    """
    ollama를 이용하여 qwen으로 inference를 수행 (스트리밍 지원)
    """
    if history is None:
        history = database.get_history()
    
    # 사용자 메시지 추가 (이미 DB에 저장되었으므로 여기서는 히스토리 리스트 구성용)
    # 실제 요청 시에는 히스토리 전체를 넘겨야 함
    
    full_history = history + [{'role': 'user', 'content': prompt}]

    # inference 수행 (stream=True)
    stream = ollama.chat(model=model, messages=full_history, stream=True)
    
    full_response = ""
    for chunk in stream:
        content = chunk['message']['content']
        full_response += content
        yield content

    # 어시스턴트 응답 DB 저장
    database.save_message('assistant', full_response)
