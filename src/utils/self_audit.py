import sys, os
sys.path.append(os.getcwd())
from src.agents.coder import CoderAgent
from src.agents.qa import QAAgent

def perform_self_audit():
    try:
        coder = CoderAgent()
        qa = QAAgent()
        print("🔍 Iniciando Auto-Auditoria de Código...")
        files_to_audit = ['src/agents/base.py', 'src/gateway/router.py']
        for file_path in files_to_audit:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f: code = f.read()
                prompt = "Analise este código para segurança e performance: " + code
                report = qa.process(prompt)
                with open('data/audit_reports.log', 'a') as f:
                    f.write(f"--- Audit for {file_path} ---\n{report}\n")
        print("✅ Auditoria concluída.")
    except Exception as e:
        print(f"❌ Erro na auditoria: {e}")

if __name__ == '__main__':
    perform_self_audit()
