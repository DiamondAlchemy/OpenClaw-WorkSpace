#!/bin/bash
set -euo pipefail

# =============================================================================
# OpenClaw Bootstrap Script — Zero to MoneyPenny in one command
# =============================================================================
#
# Usage:
#   curl -sL <this-file-url> | bash          # Full auto (after GitHub auth)
#   bash bootstrap.sh                         # Run locally
#   bash bootstrap.sh --skip-brew             # Skip Homebrew install
#   bash bootstrap.sh --backup-file /path.tar.gz  # Use local backup instead of Drive
#
# Prerequisites:
#   - macOS with admin access
#   - GitHub access to topsecretM/OpenClaw-WorkSpace (PAT or SSH key)
#   - Google account access for gog CLI auth (or a local backup file)
#
# What this does:
#   1. Installs system deps (Node.js 22+, Python 3, git, gog CLI)
#   2. Installs OpenClaw globally via npm
#   3. Clones workspace from GitHub
#   4. Restores config/credentials/database from Google Drive backup
#   5. Installs Python packages
#   6. Restores crontab entries
#   7. Starts the gateway and runs health checks
#
# =============================================================================

OPENCLAW_DIR="$HOME/.openclaw"
WORKSPACE_DIR="$OPENCLAW_DIR/workspace"
GITHUB_REPO="https://github.com/topsecretM/OpenClaw-WorkSpace.git"
DRIVE_BACKUP_FOLDER="moneypenny-bidaily-backups"
SKIP_BREW=false
BACKUP_FILE=""

# Parse args
while [[ $# -gt 0 ]]; do
    case "$1" in
        --skip-brew) SKIP_BREW=true; shift ;;
        --backup-file) BACKUP_FILE="$2"; shift 2 ;;
        *) echo "Unknown arg: $1"; exit 1 ;;
    esac
done

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

log()  { echo -e "${CYAN}[BOOTSTRAP]${NC} $1"; }
ok()   { echo -e "${GREEN}[OK]${NC} $1"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
fail() { echo -e "${RED}[FAIL]${NC} $1"; exit 1; }

# =============================================================================
# Phase 1: System Dependencies
# =============================================================================
log "Phase 1: System Dependencies"

if [ "$SKIP_BREW" = false ]; then
    # Homebrew
    if ! command -v brew &>/dev/null; then
        log "Installing Homebrew..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    ok "Homebrew ready"

    # Node.js
    if ! command -v node &>/dev/null || [[ $(node -v | sed 's/v//;s/\..*//') -lt 22 ]]; then
        log "Installing Node.js 22+..."
        brew install node
    fi
    ok "Node.js $(node -v)"

    # Python 3
    if ! command -v python3 &>/dev/null; then
        log "Installing Python 3..."
        brew install python3
    fi
    ok "Python $(python3 --version | awk '{print $2}')"

    # Git
    if ! command -v git &>/dev/null; then
        log "Installing Git..."
        brew install git
    fi
    ok "Git $(git --version | awk '{print $3}')"

    # gog CLI (Google Drive)
    if ! command -v gog &>/dev/null; then
        warn "gog CLI not found. Install it manually for Google Drive backup/restore."
        warn "Skipping Drive restore — use --backup-file instead if you have a local backup."
        GOG_AVAILABLE=false
    else
        GOG_AVAILABLE=true
        ok "gog CLI ready"
    fi
else
    log "Skipping Homebrew (--skip-brew). Checking existing tools..."
    command -v node &>/dev/null || fail "Node.js not found"
    command -v python3 &>/dev/null || fail "Python 3 not found"
    command -v git &>/dev/null || fail "Git not found"
    GOG_AVAILABLE=false
    command -v gog &>/dev/null && GOG_AVAILABLE=true
    ok "All required tools present"
fi

# =============================================================================
# Phase 2: Install OpenClaw
# =============================================================================
log "Phase 2: Install OpenClaw"

if ! command -v openclaw &>/dev/null; then
    log "Installing OpenClaw via npm..."
    npm install -g openclaw
fi
ok "OpenClaw $(openclaw --version 2>/dev/null || echo 'installed')"

# Create base directory
mkdir -p "$OPENCLAW_DIR"

# =============================================================================
# Phase 3: Clone Workspace from GitHub
# =============================================================================
log "Phase 3: Clone Workspace"

if [ -d "$WORKSPACE_DIR/.git" ]; then
    log "Workspace already exists, pulling latest..."
    cd "$WORKSPACE_DIR" && git pull origin main
    ok "Workspace updated"
else
    log "Cloning from GitHub..."
    git clone "$GITHUB_REPO" "$WORKSPACE_DIR"
    ok "Workspace cloned"
fi

# =============================================================================
# Phase 4: Restore Config & Credentials from Backup
# =============================================================================
log "Phase 4: Restore Config & Credentials"

if [ -n "$BACKUP_FILE" ]; then
    # Use provided local backup
    if [ ! -f "$BACKUP_FILE" ]; then
        fail "Backup file not found: $BACKUP_FILE"
    fi
    log "Extracting from local backup: $BACKUP_FILE"
    tar -xzf "$BACKUP_FILE" -C /
    ok "Restored from local backup"

elif [ "$GOG_AVAILABLE" = true ]; then
    log "Fetching latest backup from Google Drive..."

    # Find the backup folder
    FOLDER_ID=$(gog drive ls --plain --query "name = '${DRIVE_BACKUP_FOLDER}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false" | tail -n +2 | head -n 1 | awk '{print $1}')

    if [ -z "$FOLDER_ID" ]; then
        fail "Google Drive folder '${DRIVE_BACKUP_FOLDER}' not found. Authenticate gog or use --backup-file."
    fi

    # Get the most recent backup file
    LATEST_BACKUP=$(gog drive ls --plain --query "'${FOLDER_ID}' in parents and trashed = false" --orderBy "createdTime desc" | tail -n +2 | head -n 1)
    BACKUP_ID=$(echo "$LATEST_BACKUP" | awk '{print $1}')
    BACKUP_NAME=$(echo "$LATEST_BACKUP" | awk '{$1=""; print $0}' | xargs)

    if [ -z "$BACKUP_ID" ]; then
        fail "No backups found in Drive folder. Use --backup-file with a local backup."
    fi

    log "Downloading: $BACKUP_NAME"
    TEMP_BACKUP="/tmp/openclaw-restore-$$.tar.gz"
    gog drive download "$BACKUP_ID" -o "$TEMP_BACKUP"

    log "Extracting backup..."
    tar -xzf "$TEMP_BACKUP" -C /
    rm -f "$TEMP_BACKUP"
    ok "Restored from Drive backup: $BACKUP_NAME"

else
    warn "No backup source available."
    warn "To complete setup, you need either:"
    warn "  1. Install gog CLI and authenticate, then re-run this script"
    warn "  2. Re-run with: bash bootstrap.sh --backup-file /path/to/backup.tar.gz"
    warn ""
    warn "Without backup, the following are MISSING:"
    warn "  - openclaw.json (API keys, Telegram tokens, gateway config)"
    warn "  - credentials/ (Telegram/WhatsApp pairing)"
    warn "  - identity/ (device keys)"
    warn "  - lcm.db (conversation history/context)"
    warn "  - Agent workspaces (octopussy, q, shared, goldfinger)"
    warn ""
    warn "Continuing with workspace-only setup..."
fi

# =============================================================================
# Phase 5: Verify Critical Files
# =============================================================================
log "Phase 5: Verify Critical Files"

MISSING=0
check_file() {
    if [ -e "$1" ]; then
        ok "  $1"
    else
        warn "  MISSING: $1"
        MISSING=$((MISSING + 1))
    fi
}

check_file "$OPENCLAW_DIR/openclaw.json"
check_file "$OPENCLAW_DIR/identity/device.json"
check_file "$OPENCLAW_DIR/credentials/telegram-pairing.json"
check_file "$OPENCLAW_DIR/lcm.db"
check_file "$OPENCLAW_DIR/workspace/SOUL.md"
check_file "$OPENCLAW_DIR/workspace/MEMORY.md"
check_file "$OPENCLAW_DIR/workspace-octopussy/SOUL.md"
check_file "$OPENCLAW_DIR/workspace-q/SOUL.md"
check_file "$OPENCLAW_DIR/workspace-shared/SOUL.md"
check_file "$OPENCLAW_DIR/workspace-goldfinger/SOUL.md"
check_file "$OPENCLAW_DIR/cron/jobs.json"

if [ $MISSING -gt 0 ]; then
    warn "$MISSING files missing — backup may not have restored fully"
fi

# =============================================================================
# Phase 6: Python Dependencies
# =============================================================================
log "Phase 6: Python Dependencies"

pip3 install --quiet anthropic telethon aiohttp 2>/dev/null || warn "Some pip installs failed (non-critical)"
ok "Python packages installed"

# =============================================================================
# Phase 7: Restore Crontab
# =============================================================================
log "Phase 7: Restore Crontab"

CRONTAB_CONTENT='DUNE_API_KEY=sRkvZDsjRkjkLWsbrnQMRSBX1hu54amu
GOLDFINGERS_TG_TOKEN=8714972612:AAFDrOXrCnfPmG8t4YI_jOMp2pqTAtPTi9c
GOLDFINGERS_TG_CHAT_ID=8217045820

# Telegram scrapes (every 6 hours)
0 6,10,14,18,22,2 * * * /Users/m/.openclaw/workspace-shared/scrapes/run_scrapes.sh

# Goldfingers Perp Tracker — discovery + profile (every 6 hours)
0 */6 * * * cd /Users/m/.openclaw/workspace-goldfinger/perp_tracker && /usr/bin/python3 perp_tracker.py discover --config config.json >> logs/cron_discover.log 2>&1
10 */6 * * * cd /Users/m/.openclaw/workspace-goldfinger/perp_tracker && /usr/bin/python3 perp_tracker.py profile --config config.json >> logs/cron_profile.log 2>&1

# Morning intel report (6am daily)
0 6 * * * cd /Users/m/.openclaw/workspace-goldfinger/perp_tracker && /usr/bin/python3 -c "from perp_tracker import PerpTracker, load_config; import asyncio; config = load_config('"'"'config.json'"'"'); t = PerpTracker(config); report = t.generate_report(); asyncio.run(t.alerter.send(report)); t.close()" >> logs/cron_morning.log 2>&1

# Sunday 10pm: deep scrape + shadow desk hunt
0 22 * * 0 cd /Users/m/.openclaw/workspace-goldfinger/perp_tracker && /usr/bin/python3 scrape_leaderboard.py --limit 50 >> logs/cron_scrape.log 2>&1
30 22 * * 0 cd /Users/m/.openclaw/workspace-goldfinger/perp_tracker && /usr/bin/python3 perp_tracker.py discover --config config.json >> logs/cron_scrape.log 2>&1

# Sunday 11pm: autonomous engine
0 23 * * 0 cd /Users/m/.openclaw/workspace-goldfinger/Hunting\ Grounds && /usr/bin/python3 autonomous_engine.py --budget 200 >> logs/cron_autonomous.log 2>&1
'

# Check if crontab already has openclaw entries
if crontab -l 2>/dev/null | grep -q "openclaw"; then
    warn "Crontab already has openclaw entries — skipping to avoid duplicates"
    warn "To force replace, run: echo \"\$CRONTAB_CONTENT\" | crontab -"
else
    echo "$CRONTAB_CONTENT" | crontab -
    ok "Crontab restored ($(echo "$CRONTAB_CONTENT" | grep -c '^\*\|^[0-9]') jobs)"
fi

# =============================================================================
# Phase 8: Start Gateway & Health Check
# =============================================================================
log "Phase 8: Start Gateway"

if [ -f "$OPENCLAW_DIR/openclaw.json" ]; then
    log "Starting OpenClaw gateway..."
    openclaw gateway start &
    GATEWAY_PID=$!
    sleep 5

    if kill -0 $GATEWAY_PID 2>/dev/null; then
        ok "Gateway started (PID: $GATEWAY_PID, port 18789)"
    else
        warn "Gateway may have failed to start — check logs"
    fi

    log "Running health check..."
    openclaw doctor 2>&1 || warn "Doctor reported issues (check output above)"
else
    warn "openclaw.json missing — cannot start gateway"
    warn "Restore from backup first, then run: openclaw gateway start"
fi

# =============================================================================
# Done
# =============================================================================
echo ""
echo -e "${GREEN}============================================${NC}"
echo -e "${GREEN}  OpenClaw Bootstrap Complete${NC}"
echo -e "${GREEN}============================================${NC}"
echo ""
echo "Next steps:"
echo "  1. Verify Telegram: send a message to @MoneyPenny_openclawbot"
echo "  2. Check gateway: curl http://localhost:18789/health"
echo "  3. Review config: cat ~/.openclaw/openclaw.json"
echo ""
if [ $MISSING -gt 0 ]; then
    echo -e "${YELLOW}  ⚠ $MISSING files were missing — check warnings above${NC}"
fi
