from utils.system_utils import env_loader
from utils.ai_utils import ollama_inference

def main():
    request = "안녕하세요."
    response = ollama_inference(request)
    print(f"응답: {response}")

if __name__ == "__main__":
    main()
