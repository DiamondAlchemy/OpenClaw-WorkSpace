# Workspace Dossier: Money Penny's Operational Bible

This document is the central reference for Alvie's OpenClaw setup, managed by Money Penny. It is a living document and will be updated as the system evolves.

## 1. Active Missions & Priorities

### Phase 1: Core Operations
*   **Visual Extraction Manifest:** Mastering the master spreadsheet for KPIs and logistics. Includes walkthroughs and data entry protocol establishment. **(Status: Active)**
*   **Money Penny Infrastructure:** Hardening security, optimizing memory, and ensuring long-term stability. **(Status: Active)**
*   **GMP Framework (Christian):** Monitoring and data gathering for US/EU-GMP lab qualification. No direct infrastructure changes without Alvie's approval. **(Status: Standby)**

### Future & Backlog
*   **Intelligence Archive:** Maintain and expand the archive at `/Users/m/Desktop/MoneyPenny_Intelligence`.
*   **Financial Ops:** Plan for future integration with Christian's financial ventures.
*   **Expansion:** Prepare for supporting international operations.

---

## 2. Platform Configuration

### OpenClaw Core
- **Workspace:** `~/.openclaw/workspace`
- **Gateway Mode:** Local
- **Gateway Port:** 18789
- **Authentication:** Token-based with rate limiting.

### Memory System (Hybrid Strategy)
- **Status:** Active
- **Provider:** Native Local Search
- **Model:** `hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf`
- **Protocol:** "Smart Loading" is enabled. `MEMORY.md` is not loaded into context on startup; the `memory_search` tool is used for recall instead.

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
- **Routing:** Model set in main OpenClaw config. No advanced routing rules in place.

---

## 5. Active Cron Jobs

| Name                 | Schedule                | Action                                                       |
| :------------------- | :---------------------- | :----------------------------------------------------------- |
| **Daily Self-Review**  | `0 8 * * *` (8am CT)      | Scans core files for inconsistencies and reports findings.     |
| **Daily Security Audit** | `0 9 * * *` (9am)       | Performs a deep security audit of the OpenClaw installation. |
| **Memory Curator**     | `0 9 * * 1,4` (9am CT M/Th) | Runs `memory_curator.py` to manage and archive memory files. |

---

## 6. Backup Procedures

A manual script is in place for backups.

- **Script:** `backup_to_drive.sh`
- **Action:** Compresses the workspace (`~/.openclaw/workspace`) into a timestamped `.tar.gz` archive and uploads it to a specific Google Drive folder using the `gog` CLI.
- **Frequency:** Automated. The cron schedule runs this script twice daily at 4:00 AM and 4:00 PM.

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

### Core Skills (Documented in AGENTS.md)
- **gog:** Google Workspace CLI (Gmail, Calendar, Drive, Sheets, Docs)
- **github:** GitHub CLI (issues, PRs, CI, code review)
- **healthcheck:** Host security hardening and risk audits
- **peekaboo:** macOS UI automation (use with caution)
- **summarize:** Summarize text from URLs, podcasts, files
- **tts:** Text-to-Speech for voice output
- **weather:** Weather forecasts via wttr.in/Open-Meteo
- **xurl:** X (Twitter) API CLI

### Productivity & Notes
- **obsidian:** Work with Obsidian vaults (Markdown notes)
- **things-mac:** Manage Things 3 tasks via CLI
- **apple-notes:** Apple Notes via memo CLI
- **imsg:** iMessage/SMS via Messages.app

### Data & Analysis
- **nano-pdf:** Edit PDFs with natural-language instructions
- **video-frames:** Extract frames/clips from videos (ffmpeg)

### Communication
- **wacli:** WhatsApp CLI (send messages, search/sync)
- **discord:** Discord bot interactions
- **slack:** Slack bot interactions

### Other Installed (Not Yet Explored)
- apple-reminders, bear-notes, blogwatcher, blucli, bluebubbles, camsnap, canvas, clawhub, coding-agent, eightctl, gemini, gh-issues, gifgrep, goplaces, himalaya, mcporter, model-usage, nano-banana-pro, notion, openai-image-gen, openai-whisper, openai-whisper-api, openhue, oracle, ordercli, sag, session-logs, sherpa-onnx-tts, skill-creator, songsee, sonoscli, spotify-player, tmux, trello, voice-call

*(Note: This list is periodically verified. Run `openclaw skills list` to refresh.)*

---

## 8. Established Conventions

- **Data Integrity Protocol:** Catalog all critical information (decisions, facts, updates) from conversations into daily memory logs (`memory/YYYY-MM-DD.md`) to ensure persistence across session resets. Use tags like `[DECISION]`, `[FACT]`, etc.
- **Chain of Command:** All infrastructure changes require direct approval from Alvie.
- **Heartbeats:** Proactive checks for email/calendar/files. Triggered by external poll events (~4h intervals). Reply `HEARTBEAT_OK` if clear.
- **Workspace Reference:** This `WORKSPACE.md` file is to be maintained as the single source of truth for the system's configuration and operational procedures.
