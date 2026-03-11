#!/bin/bash
# Agent Workspace Backup Script
# Zips Q and Octopussy workspaces, uploads to Drive, and saves to Desktop

BACKUP_DIR="$HOME/Desktop/TopSecretBackups"
DRIVE_FOLDER_ID="1G_ms1hedCxglsxCynqfPhIYlCccIgLvu"
TIMESTAMP=$(date +%Y-%m-%d_%H%M)

# Create backup dir if needed
mkdir -p "$BACKUP_DIR"

# Backup Q workspace
echo "Backing up Q workspace..."
zip -r "$BACKUP_DIR/q_workspace_$TIMESTAMP.zip" /Users/m/.openclaw/workspace-q/ -x "*.DS_Store"

# Backup Octopussy workspace
echo "Backing up Octopussy workspace..."
zip -r "$BACKUP_DIR/octopussy_workspace_$TIMESTAMP.zip" /Users/m/.openclaw/workspace-octopussy/ -x "*.DS_Store"

# Backup shared folder
echo "Backing up shared folder..."
zip -r "$BACKUP_DIR/shared_$TIMESTAMP.zip" /Users/m/.openclaw/workspace/shared/ -x "*.DS_Store"

# Upload to Drive
echo "Uploading to Drive..."
gog drive upload "$BACKUP_DIR/q_workspace_$TIMESTAMP.zip" --parent "$DRIVE_FOLDER_ID"
gog drive upload "$BACKUP_DIR/octopussy_workspace_$TIMESTAMP.zip" --parent "$DRIVE_FOLDER_ID"
gog drive upload "$BACKUP_DIR/shared_$TIMESTAMP.zip" --parent "$DRIVE_FOLDER_ID"

# Cleanup local backups older than 7 days
find "$BACKUP_DIR" -name "*.zip" -mtime +7 -delete

echo "Backup complete: $TIMESTAMP"
