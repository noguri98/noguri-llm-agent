from utils.system_utils import env_loader

def main():
    env = env_loader()
    obsidian_path = env["OBSIDIAN_PATH"]
    agent_docs_path = env["AGENT_DOCS_PATH"]
    
    print(obsidian_path)
    print(agent_docs_path)
if __name__ == "__main__":
    main()
