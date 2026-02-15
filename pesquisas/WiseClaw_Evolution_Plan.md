
# WiseClaw Evolution Plan: From Factory to Ecosystem
*Based on Stanford, MIT, and Harvard Research (2026)*

## 1. Strategic Pillars
### A. The "Live Context" Backbone (Implemented)
- **Concept:** Shared, read-heavy state for all agents.
- **Validation:** Aligns with LinkedIn engineering advice to "be cautious with write-heavy workflows" and favor shared state for reading.
- **Next Step:** Expand `live_context.md` to include "Active Tasks" and "Blockers" dynamically updated by the Manager.

### B. Agent Lifecycle Management (ALM)
- **Concept:** Structured process for designing, deploying, and monitoring agents.
- **Source:** OneReach.ai & Harvard Business Review.
- **Action:** Implement a "Health Check" protocol where agents report their status (Idle, Busy, Error) to a central dashboard (Telegram Mini App).

### C. Structured Inter-Agent Communication
- **Concept:** Agents must agree on the "shape" of information.
- **Source:** Stack AI.
- **Action:** Define strict JSON schemas for agent-to-agent handoffs (e.g., Manager -> Coder must follow a specific `TaskSpec` format).

## 2. Proposed Roadmap
### Phase 1: The Dashboard (Observability)
- Create a Telegram Mini App (Web App) that reads `live_context.md` and agent logs to show a real-time status board.

### Phase 2: The Protocol (Standardization)
- Implement `pydantic` models for all agent outputs to ensure strict typing and reduce hallucinations during handoffs.

### Phase 3: The Hive (Swarm Intelligence)
- Allow agents to "vote" on decisions. For example, the Coder proposes a fix, the Critic reviews it, and the Manager casts the deciding vote based on the "Constitution" (System Prompt).

## 3. Immediate Action Items
1. **Refine Live Context:** Add sections for `Current_Sprint` and `System_Health`.
2. **Standardize Logs:** Ensure all agents log in a machine-readable format (JSON lines) for the dashboard to consume.
3. **Knowledge Ingestion:** Feed this plan into the Librarian.
