# 🦁 WiseClaw Evolution Strategy: The "Trust but Verify" Era

## 1. Diagnosis: The "Reactive" Trap
Currently, our agents are functional but reactive. They wait for commands and execute them linearly. To achieve **fluidity** and **intelligence**, we must shift to a **Proactive & Audited** model.

---

## 2. Upgrading the Core Squad (Level Up)

| Agent | Current State | **Evolved Role** | **New Superpower (Auditability)** |
| :--- | :--- | :--- | :--- |
| **Manager** | Task Delegator | **Product Owner (PO)** | Defines **Acceptance Criteria** (Definition of Done) before work starts. Rejects work that doesn't match. |
| **Researcher** | Web Searcher | **Investigative Journalist** | Must provide **Citations** (URLs/Files) for every claim. Uses "Recursive Search" (Search -> Read -> Verify -> Search Again). |
| **Coder** | Script Writer | **TDD Engineer** | Writes **Tests** before Code. Uses strict typing (Pydantic) to ensure data structures are valid. |
| **Critic** | Reviewer | **Compliance Auditor** | Validates against the **Constitution** (CO-STAR) and Security Policies (OWASP). |

---

## 3. New Agents: The "Elite" Specialists

### 🛡️ A. The Sentinel (Security & Governance)
*   **Role:** The Gatekeeper.
*   **Mission:** Prevent data leaks and unsafe operations.
*   **Tools:** `bandit` (SAST), `safety` (dependency check), Regex for PII masking.
*   **Workflow:** Intercepts every file write and terminal command. If it detects a secret key or dangerous commands, it blocks execution.

### 🧪 B. The QA Engineer (Quality Assurance)
*   **Role:** The Breaker.
*   **Mission:** Prove the Coder wrong.
*   **Tools:** `pytest`, `hypothesis` (property-based testing).
*   **Workflow:** Takes the Coder's output and runs edge-case inputs. Generates a **Test Report** (Pass/Fail) for the Dashboard.

### 🧠 C. The Archivist (Knowledge Graph)
*   **Role:** The Connector.
*   **Mission:** Connect dots between isolated memories.
*   **Tools:** Graph RAG (Nodes & Edges).
*   **Workflow:** Instead of just storing text, it maps relationships (e.g., "Streamlit" --is_used_for--> "Dashboard"). Proactively fetches context for other agents.

---

## 4. The "War Room" Workflow (Fluidity)

Instead of linear ping-pong, we adopt a state-machine flow:

1.  **Planning Phase:** Manager & Researcher define the *Plan* and *Acceptance Criteria*.
2.  **Build Phase:** Coder & Archivist execute. Coder writes tests first.
3.  **Audit Phase:** QA runs the tests. Sentinel scans the code.
4.  **Release Phase:** Only if Audit passes, the Manager presents the result to the User.
