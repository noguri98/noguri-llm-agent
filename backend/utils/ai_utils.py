import ollama
import json
import os

HISTORY_FILE = "conversation.json"

def load_history() -> list:
    """JSON 파일에서 대화 히스토리를 로드"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []

def save_history(history: list):
    """대화 히스토리를 JSON 파일에 저장"""
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def ollama_inference(prompt: str, model: str = "qwen3:8b", history: list = None) -> tuple[str, list]:
    """
    ollama를 이용하여 qwen으로 inference를 수행 (히스토리 포함)
    
    Args:
        prompt: 입력 프롬프트
        model: 사용할 모델명 (기본값: "qwen3:8b")
        history: 대화 히스토리 리스트 (None이면 파일에서 로드)
    
    Returns:
        (응답 텍스트, 업데이트된 히스토리) 튜플
    """
    if history is None:
        history = load_history()
    
    # 사용자 메시지 추가
    history.append({
        'role': 'user',
        'content': prompt,
    })
    
    # inference 수행
    response = ollama.chat(model=model, messages=history)
    assistant_message = response['message']['content']
    
    # 어시스턴트 응답 추가
    history.append({
        'role': 'assistant',
        'content': assistant_message,
    })
    
    # 히스토리 저장
    save_history(history)
    
    return assistant_message, history
