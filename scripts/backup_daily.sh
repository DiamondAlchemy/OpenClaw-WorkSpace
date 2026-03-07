#!/bin/bash
# OpenClaw Daily Backup Script
# Creates timestamped backups of all agent workspaces

DATE=$(date +%Y-%m-%d)
BACKUP_DIR="$HOME/Backups/OpenClaw/daily/$DATE"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup main workspace
cd ~/.openclaw
zip -r "$BACKUP_DIR/main_workspace.zip" workspace/ > /dev/null 2>&1

# Backup Octopussy workspace
zip -r "$BACKUP_DIR/octopussy_workspace.zip" workspace-octopussy/ > /dev/null 2>&1

# Backup Q workspace
zip -r "$BACKUP_DIR/q_workspace.zip" workspace-q/ > /dev/null 2>&1

# Backup config
cp ~/.openclaw/openclaw.json "$BACKUP_DIR/openclaw.json"

# Cleanup old backups (keep last 7 days)
find "$HOME/Backups/OpenClaw/daily" -type d -mtime +7 -exec rm -rf {} \; 2>/dev/null

echo "Backup completed: $DATE"
