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
