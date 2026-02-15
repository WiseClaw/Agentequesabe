# WiseClaw System Knowledge Base (2026)

## 1. System Architecture: Hybrid Brain
- **Core Logic:** The system uses a "Hybrid Brain" approach via a Gateway Router.
- **Models:**
  - **Manager/Coder/Operator:** Claude 3.5 Sonnet (Anthropic) - Best for logic, coding, and complex instructions.
  - **Researcher:** Gemini 3 Pro (Google) - Best for deep research and large context windows (2M tokens).
  - **Auditor:** GPT-4o (OpenAI) - Best for diverse perspective and critique.

## 2. Platform Capabilities & Strategy
### Discord (The Headquarters)
- **Role:** Central Hub for heavy lifting, team management, and state tracking.
- **Structure:**
  - **Specialized Channels:** #investigacao (Researcher), #dev-lab (Coder), #auditoria (Critic).
  - **General Channels:** #geral, #offtopic -> Mapped to **Manager** (Omnipresent Mode).
- **Key Features to Exploit:**
  - **Gateway API:** Real-time event listening for moderation.
  - **Threads/Forums:** Auto-organization of knowledge.
  - **Voice API:** Meeting transcription and audio analysis.

### Telegram (The Mobile Terminal)
- **Role:** Agile command center and mobile interface.
- **Key Features to Exploit:**
  - **Mini Apps:** HTML5 Web Apps inside chat for visual dashboards.
  - **Webhooks:** Low-latency notifications.
  - **Topics:** Organizing supergroups similarly to Discord channels.

## 3. Operational Protocols
- **Omnipresent Manager:** The Discord bot is configured to default to the 'Manager' agent for any channel not explicitly mapped to a specialist. This ensures responsiveness everywhere.
- **Memory:** The system uses ChromaDB (Librarian) for long-term memory. Documents in 'pesquisas/' are ingested and retrievable by agents.
- **Research:** The Researcher agent is equipped with 'ddgs' (DuckDuckGo) and 'trafilatura' for live web deep dives.

## 4. Current Status (Feb 2026)
- Bots are online on both platforms.
- "Factory" structure is active.
- Memory ingestion is manual via 'src/librarian/ingest.py'.
