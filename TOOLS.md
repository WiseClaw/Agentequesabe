# TOOLS.md - OpenClaw Workspace Reference

## 1. System Identity
- **Name:** WiseClaw (The Architect)
- **Role:** Autonomous Orchestrator
- **Framework:** Agent Zero / OpenClaw Architecture

## 2. Active Agents & Tools
### Librarian (Memory)
- **Path:** `src/librarian/`
- **Function:** Ingests PDFs, manages ChromaDB vector store.
- **Scripts:**
  - `ingest.py`: Indexes new documents from `pesquisas/`.
  - `query.py`: Retrieves context based on semantic search.

### Gateway (Efficiency)
- **Path:** `src/gateway/`
- **Function:** Routes tasks to appropriate models to save tokens.

### Interfaces (Connectivity)
- **Path:** `src/interfaces/`
- **Function:** External communication channels.
- **Scripts:**
  - `telegram_bot.py`: Connects to Telegram Bot (@Agentequesabot).
  - `discord_bot.py`: Connects to Discord Application.

## 3. Infrastructure
- **Version Control:** Git (Local Repository initialized)
- **Memory:** ChromaDB (Local Vector Store)
- **Logs:** `wiseclawolf_log.md`

## 4. Current Status
- [x] Librarian Agent (Basic Ingestion/Query)
- [x] Local Backup (Git Init)
- [x] Gateway Router (Prototype)
- [x] Telegram Interface (Configured & Verified)
- [x] Discord Interface (Configured)
- [ ] Cloud Backup (Drive/S3)
