import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from agents.operator import OperatorAgent

op = OperatorAgent()
print("--- Testando MCP via Operator ---")
files = op.execute_mcp_tool("list_directory", {"path": "."})
print(f"Ficheiros detetados via MCP: {files[:5]}...")

report_content = f"Relatório de Sistema - Ficheiros encontrados: {len(files)}"
status = op.execute_mcp_tool("write_file", {"path": "data/system_health.json", "content": report_content})
print(f"Status da escrita via MCP: {status}")
