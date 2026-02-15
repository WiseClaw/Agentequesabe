# 🦁 WiseClaw System State Summary (2026-02-15)

## 1. Architecture: Hybrid Brain 2.1 (Fallback Chains)
- **Main Chain (Manager):** Opus -> Sonnet -> Gemini Pro -> Gemini Flash -> Haiku
- **Subagent Chain (Coder, QA, etc.):** Sonnet -> Gemini Flash -> Haiku -> Gemini Pro

## 2. Workflow: The "War Room"
- **Manager:** Orchestrator (Uses Main Chain).
- **Coder:** TDD Engineer (Uses Subagent Chain).
- **Sentinel:** Security Auditor (Uses Subagent Chain).
- **QA:** Test Runner (Uses Subagent Chain).

## 3. Status
- **System:** Active
- **Backup:** Synced to GitHub
