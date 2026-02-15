from src.agents.sentinel import SentinelAgent
from src.agents.qa import QAAgent

print("🦁 --- WiseClaw War Room Simulation ---")

# 1. Initialize Agents
sentinel = SentinelAgent()
qa = QAAgent()

# Scenario A: Unsafe Code
unsafe_code = """
import os
def delete_everything():
    os.system('rm -rf /')
"""
print("\n[1] Testing Sentinel with UNSAFE code...")
audit = sentinel.audit_code(unsafe_code)
print(f"Result: {audit['status']} - {audit['report']}")

# Scenario B: Safe Code & QA
safe_code = """
def add(a, b):
    return a + b
"""
test_code = """
from candidate import add
def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
"""

print("\n[2] Testing Sentinel with SAFE code...")
audit = sentinel.audit_code(safe_code)
print(f"Result: {audit['status']}")

if audit['status'] == 'SAFE':
    print("\n[3] Passing to QA Agent for Testing...")
    result = qa.run_test_cycle(safe_code, test_code)
    print("QA Result:")
    print(result)
