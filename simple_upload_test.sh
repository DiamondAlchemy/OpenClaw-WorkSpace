#!/bin/bash
echo "Creating a dummy file..."
TIMESTAMP=$(date +"%Y-%m-%d-%H%M%S")
DUMMY_FILE="/tmp/test-upload-${TIMESTAMP}.txt"
echo "This is a test file for Google Drive upload." > ${DUMMY_FILE}

echo "Attempting to upload ${DUMMY_FILE} to root of Google Drive..."
gog drive upload ${DUMMY_FILE}
