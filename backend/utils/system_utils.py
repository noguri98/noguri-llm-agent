import os

def env_loader():
    """
    /에 있는 .env 파일의 환경변수를 가져와 시스템 변수로 설정
    """
    env_path = os.getenv("ENV_PATH")
    if env_path is None:
        env_path = "../.env"
    with open(env_path, "r") as f:
        for line in f:
            if line.startswith("#"):
                continue
            if line.strip() == "":
                continue
            key, value = line.strip().split("=")
            os.environ[key] = value
    return os.environ