import sys, os, time
sys.path.append(os.getcwd())
from src.agents.manager import ManagerAgent
from src.memory.context_manager import ContextManager

def run_sentinel_loop():
    manager = ManagerAgent()
    context = ContextManager()
    print("🚀 Sentinel Loop Ativo.")
    while True:
        try:
            state = context.get_live_context()
            suggestion = manager.process(f"Analise o estado e sugira melhorias: {state}")
            with open('data/proactive_thoughts.log', 'a') as f:
                f.write(f"[{time.ctime()}] {suggestion}\n")
            time.sleep(3600)
        except Exception as e:
            print(f"Erro: {e}")
            time.sleep(60)

if __name__ == '__main__':
    run_sentinel_loop()
