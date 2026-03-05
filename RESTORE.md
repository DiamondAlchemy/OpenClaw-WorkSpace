# RESTORE.md - Disaster Recovery Protocol

**Objective:** Rebuild Money Penny (OpenClaw instance) from scratch in the event of total system loss or migration to a new host.

**Sources:**
1.  **Code & Logic:** Private GitHub Repository (`https://github.com/topsecretM/OpenClaw-WorkSpace.git`)
2.  **Data & Config:** Google Drive Backup Folder (`moneypenny-bidaily-backups`)

---

## Phase 1: Preparation

1.  **Secure New Host:** Ensure the new machine (Mac mini or Linux server) has:
    *   Git installed (`git --version`)
    *   Python 3 installed (`python3 --version`)
    *   Node.js 22+ installed (`node -v`)
    *   Google Cloud CLI / `gog` tool installed and authenticated.

2.  **Authenticate GitHub:**
    *   Generate a new Personal Access Token (PAT) on GitHub if needed.
    *   Ensure you can access the private repo.

## Phase 2: Restore Core Logic (Workspace)

1.  **Install OpenClaw:**
    ```bash
    npm install -g openclaw
    openclaw --version
    ```

2.  **Clone Workspace:**
    *   Navigate to the OpenClaw directory (create if missing):
        ```bash
        mkdir -p ~/.openclaw
        cd ~/.openclaw
        ```
    *   Clone the repository into the `workspace` folder:
        ```bash
        git clone https://github.com/topsecretM/OpenClaw-WorkSpace.git workspace
        ```

## Phase 3: Restore Data & Configuration (The Brain)

1.  **Locate Backup:**
    *   Go to Google Drive and open the folder `moneypenny-bidaily-backups`.
    *   Download the latest `.tar.gz` archive (e.g., `openclaw-backup-2026-03-04-100000.tar.gz`).
    *   Place this file in your home directory (`~/`).

2.  **Extract Data:**
    *   **WARNING:** This will overwrite existing OpenClaw data. Ensure `~/.openclaw` is empty or backed up if this is not a fresh install.
    *   Extract the archive (note: the `-C /` flag extracts relative to the root directory, which is what we want since the archive contains the full path from `/Users/m`):
        ```bash
        tar -xzf ~/openclaw-backup-YYYY-MM-DD-HHMMSS.tar.gz -C /
        ```

3.  **Verify Configuration:**
    *   Check `~/.openclaw/openclaw.json`. This file contains your API keys, Telegram tokens, and Gateway settings. It was **excluded** from GitHub but **included** in the Google Drive backup.

## Phase 4: Reconnect Integrations

1.  **Telegram:**
    *   The bot token is in `openclaw.json`. OpenClaw should automatically reconnect upon startup.
    *   Send a test message to `@MoneyPenny_openclawbot` to confirm.

2.  **Cron Jobs:**
    *   Re-install the crontab entries for backups and self-review:
        ```bash
        (crontab -l 2>/dev/null; echo "0 8 * * * /Users/m/.openclaw/workspace/run_daily_self_review.sh") | crontab -
        (crontab -l 2>/dev/null; echo "0 4,16 * * * /Users/m/.openclaw/workspace/backup_to_drive.sh") | crontab -
        ```

## Phase 5: Verification

1.  **Start OpenClaw:**
    ```bash
    openclaw gateway start
    ```
2.  **Health Check:**
    ```bash
    openclaw doctor
    ```
3.  **Test Memory:**
    *   Ask: "What is the mission regarding Top Secret Workshops?"
    *   Verify it retrieves the correct context from `MEMORY.md`.

---
*Architecture Credit: Matthew Berman's OpenClaw Deep Dive*
