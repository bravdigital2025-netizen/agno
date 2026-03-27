# Jarvis — Test Log

---

### demo.py

**Status:** PENDING

**Description:** Full Jarvis orchestration demo. Runs four sample queries against all five specialist agents (Inventory, Marketing, WhatsApp, Projects, Reports) via the main Team coordinator.

**Prerequisites:**
- PostgreSQL running via `./cookbook/scripts/run_pgvector.sh`
- `ANTHROPIC_API_KEY` set
- `WHATSAPP_ACCESS_TOKEN` + `WHATSAPP_PHONE_NUMBER_ID` set (for marketing/whatsapp agents)

**Run:**
```bash
.venvs/demo/bin/python cookbook/jarvis/demo.py
```

**Result:** Not yet tested.

---
