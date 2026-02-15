from src.agents.manager import ManagerAgent
import os

manager = ManagerAgent()
task = "Crie uma função em python que valide se uma string é um e-mail válido. Use regex. Inclua testes para casos válidos e inválidos."

print("--- INICIANDO FLUXO WAR ROOM (FASE B) ---")
result = manager.process(task)
print("\n--- RESULTADO FINAL ---")
print(result)
