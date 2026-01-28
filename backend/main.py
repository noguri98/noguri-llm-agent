import sys
import io
from utils.system_utils import env_loader
from utils.ai_utils import ollama_inference

def main():
    # 터미널 인코딩을 UTF-8로 설정
    if sys.stdin.encoding != 'utf-8':
        sys.stdin = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8', errors='replace')
    if sys.stdout.encoding != 'utf-8':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("\n채팅을 시작합니다. 종료하려면 'quit' 또는 'exit'를 입력하세요.\n")
    
    while True:
        # 사용자 입력 받기
        try:
            user_input = input("질문: ").strip()
        except UnicodeDecodeError:
            print("입력 인코딩 오류가 발생했습니다. UTF-8로 다시 시도해주세요.")
            continue
        
        if not user_input:
            continue
        
        if user_input.lower() in ['quit', 'exit', '종료']:
            print("대화를 종료합니다.")
            break
        
        # inference 수행
        try:
            response, _ = ollama_inference(user_input)
            print(f"\n응답: {response}\n")
        except Exception as e:
            print(f"오류 발생: {e}\n")

if __name__ == "__main__":
    main()
