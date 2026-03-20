# Workspace Dossier: Money Penny's Operational Bible

This document is the central reference for Alvie's OpenClaw setup, managed by Money Penny. It is a living document and will be updated as the system evolves.

## 1. Active Missions & Priorities

### Phase 1: Core Operations
*   **Money Penny Infrastructure:** Hardening security, optimizing memory, and ensuring long-term stability. **(Status: Active)**
*   **GMP Framework (Christian):** Monitoring and data gathering for US/EU-GMP lab qualification. No direct infrastructure changes without Alvie's approval. **(Status: Standby)**

### Future & Backlog
*   **Intelligence Archive:** Maintain and expand the archive at `/Users/m/Desktop/MoneyPenny_Intelligence`.
*   **Financial Ops:** Plan for future integration with Christian's financial ventures.
*   **Expansion:** Prepare for supporting international operations.

---

## 2. Platform Configuration

### OpenClaw Core
- **Workspace:** `~/.openclaw/workspace` (expanded: `/Users/m/.openclaw/workspace`)
- **Data Archive:** `workspace/data-archive/` (BTC/ETH CSV files, 55MB)
- **Config File:** `openclaw.json` (located at `~/.openclaw/openclaw.json`)
- **Gateway Mode:** Local
- **Gateway Port:** 18789
- **Authentication:** Token-based with rate limiting.

### Memory System (3-Layer Architecture)

The memory system has three layers, each serving a different purpose:

#### Layer 1: Lossless Claw (Within-Session)
- **Purpose:** Handles within-session context
- **Function:** Prevents conversation history loss mid-chat
- **Status:** Fully automatic, replaces OpenClaw's default compaction
- **No scripts needed**

#### Layer 2: QMD (Retrieval Quality)
- **Purpose:** Handles retrieval quality when searching
- **Function:** Finds better results from markdown files using hybrid search
- **Status:** Fully automatic
- **No scripts needed**

#### Layer 3: Markdown Files (Cross-Session)
- **Purpose:** Source of truth for long-term memory
- **Files:** `MEMORY.md` + daily logs in `memory/YYYY-MM-DD.md`
- **Curation:** Requires scripts (see below)
- **Note:** QMD and Lossless Claw don't replace curation — they don't decide what's worth remembering long-term

##### Memory Curation Scripts

Two scripts handle curation (different philosophies):

| Script | Location | Purpose |
|--------|----------|---------|
| **memory_curator.py** | `workspace/memory_curator.py` | Guardrails Protocol — strict template, reference checking, 400-line cap, prunes old entries |
| **ai_consolidate_memory.py** | `workspace/ai_consolidate_memory.py` | Consolidation — merges logs, deduplicates facts, organizes by topic or chronologically |

Both are valid. Choose based on preference:
- Use `memory_curator.py` for strict enforcement and pruning
- Use `ai_consolidate_memory.py` for comprehensive merging and organization

---

## 3. Connected Integrations

- **Google Workspace:** Authenticated as `moneypenny@topsecretworkshops.com`. Access to Drive, Sheets, and other GSuite services is enabled via the `gog` skill.
- **Telegram:** Connected via the OpenClaw gateway. Bot handle is `@MoneyPenny_openclawbot`.

---

## 4. Model Providers & Routing

- **Primary Model:** MiniMax M2.5 High Speed (`minimax-portal/MiniMax-M2.5-highspeed`)
- **Fallback Models:**
  - Google Gemini 2.5 Flash
  - OpenAI GPT-4o Mini
  - Groq Llama 3.3-70B
  - Ollama Llama 3.2 (local)
- **Routing:** Model set in main OpenClaw config. No explicit routing rules.

### 4b. Model Capabilities & Implicit Routing

**Vision capabilities vary by model:**
- **MiniMax:** Cannot analyze images — if an image is shared, ask if they want vision analysis (requires switching to Gemini)
- **Gemini:** Can analyze images — use for photo/image tasks
- **Implicit routing:** When a task requires vision, image analysis, or screenshot reading, prefer Gemini. MiniMax handles everything else.

### 4c. Inter-Agent Messaging Protocol

To send messages between agents (Q, Octopussy, Felix), use the official messaging script:

```
python3 /Users/m/.openclaw/tools/agent_message.py <agent> "message"
```

**Available agents:**
| Agent | Bot Handle |
|-------|------------|
| main | @MoneyPenny_openclawbot |
| octopussy | @Octopussy_reporter_bot |
| q | @Q_topsecret_workshops_bot |
| Felix-The_Messenger | @Felix_topsecret_bot |

**Important:** Use this script for agent-to-agent communication — NOT internal OpenClaw spawns. This sends actual Telegram messages via the other agents' bot accounts.

---

## 5. Active Cron Jobs

| Name                 | Schedule                | Action                                                       |
| :------------------- | :---------------------- | :----------------------------------------------------------- |
| **Daily Self-Review**  | `0 8 * * *` (8am CT)      | Scans core files for inconsistencies and reports findings.     |
| **Daily Security Audit** | `0 9 * * *` (9am CT)       | Performs a deep security audit of the OpenClaw installation. |
| **Memory Curator** (Guardrails) | `0 0 * * *` (midnight CT) | Runs `memory_curator.py` — strict pruning, reference checking, 400-line cap |
| **Nightly Memory Consolidation** | `30 2 * * *` (2:30am CT) | Runs `ai_consolidate_memory.py` on workspace — merges logs, deduplicates, organizes by topic |
| **Daily GitHub Sync** | `0 15 * * *` (3pm CT) | Git add/commit/push to main |
| **Daily Agent Backup** | `0 3 * * *` (3am CT) | Runs `backup_agents.sh` — agent configuration backup |

---

## 6. Backup Procedures

Two backup scripts exist with different purposes:

### Option A: backup_to_drive.sh
- **Location:** Documented in WORKSPACE.md (may be in `/Users/m/.openclaw/` or `workspace-shared/`)
- **Purpose:** Compresses entire `~/.openclaw` directory and uploads to Google Drive
- **Target:** `moneypenny-bidaily-backups` folder in Google Drive
- **Excludes:** Socket files (`exec-approvals.sock`)
- **Frequency:** Twice daily (4:00 AM and 4:00 PM CT)
- **Use case:** Full system disaster recovery

### Option B: backup_agents.sh
- **Location:** `workspace-shared/backup_agents.sh`
- **Purpose:** Backs up agent-specific data and configurations
- **Target:** Likely Google Drive (check script for specifics)
- **Use case:** Agent configuration recovery

**Note:** These are different scripts for different purposes. `backup_to_drive.sh` is the full system backup. `backup_agents.sh` focuses on agent data. Both are worth running, or consolidate into one script if preferred.

**Script Content:**
```bash
#!/bin/bash

# A script to back up the OpenClaw directory to Google Drive.
# Version 4: Re-adds folder creation logic for clean-slate runs.

# --- Configuration ---
SOURCE_DIR_PARENT="/Users/m"
SOURCE_DIR_NAME=".openclaw"
DRIVE_FOLDER_NAME="moneypenny-bidaily-backups"
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
TEMP_ARCHIVE_PATH="/tmp/openclaw-backup-${TIMESTAMP}.tar.gz"
SOCKET_FILE_TO_EXCLUDE="${SOURCE_DIR_NAME}/exec-approvals.sock"

# --- Main Logic ---

echo "--- Starting OpenClaw Backup (v4): ${TIMESTAMP} ---"

# 1. Find or Create Google Drive Folder
echo "[1/4] Locating Google Drive folder: '${DRIVE_FOLDER_NAME}'..."
FOLDER_ID=$(gog drive ls --plain --query "name = '${DRIVE_FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false" | tail -n +2 | head -n 1 | awk '{print $1}')

if [ -z "$FOLDER_ID" ]; then
    echo "    Folder not found. Creating it now..."
    gog drive mkdir "${DRIVE_FOLDER_NAME}" > /dev/null
    # Re-query for the ID after creation, allow a moment for propagation
    sleep 2 
    FOLDER_ID=$(gog drive ls --plain --query "name = '${DRIVE_FOLDER_NAME}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false" | tail -n +2 | head -n 1 | awk '{print $1}')
    
    if [ -z "$FOLDER_ID" ]; then
        echo "    ERROR: Failed to create or find Google Drive folder after attempting creation. Aborting."
        exit 1
    fi
    echo "    Successfully created and found folder with ID: ${FOLDER_ID}"
else
    echo "    Found folder with ID: ${FOLDER_ID}"
fi


# 2. Create Compressed Archive, excluding the socket file
echo "[2/4] Creating clean compressed archive..."
tar --exclude="${SOCKET_FILE_TO_EXCLUDE}" -czf "${TEMP_ARCHIVE_PATH}" -C "${SOURCE_DIR_PARENT}" "${SOURCE_DIR_NAME}"
if [ $? -ne 0 ]; then
    echo "    ERROR: Failed to create tar archive. Aborting."
    exit 1
fi
echo "    Archive created successfully at: ${TEMP_ARCHIVE_PATH}"

# 3. Upload Archive to Google Drive
echo "[3/4] Uploading archive to Google Drive..."
UPLOAD_OUTPUT=$(gog drive upload --parent "${FOLDER_ID}" "${TEMP_ARCHIVE_PATH}")
if [[ ! "$UPLOAD_OUTPUT" == *"id"* ]]; then
    echo "    ERROR: Failed to upload to Google Drive. Local archive is preserved at ${TEMP_ARCHIVE_PATH} for review."
    exit 1
fi
echo "    Upload successful."

# 4. Clean Up Local Archive
echo "[4/4] Cleaning up local archive file..."
rm "${TEMP_ARCHIVE_PATH}"
echo "    Cleanup complete."

echo "--- Backup Process Finished Successfully ---"
```

---

## 7. Installed Skills

**Skills are documented in AGENTS.md.** That file is the canonical reference for all available skills and their usage.

*(Run `openclaw skills list` to see all installed skills.)*

---

## 8. Established Conventions

- **Data Integrity Protocol:** Catalog all critical information (decisions, facts, updates) from conversations into daily memory logs (`memory/YYYY-MM-DD.md`) to ensure persistence across session resets. Use tags like `[DECISION]`, `[FACT]`, etc.
- **Chain of Command:** All infrastructure changes require direct approval from Alvie.
- **Heartbeats:** Proactive checks for email/calendar/files. Triggered by external poll events (~4h intervals). Reply `HEARTBEAT_OK` if clear.
- **Workspace Reference:** This `WORKSPACE.md` file is to be maintained as the single source of truth for the system's configuration and operational procedures.
