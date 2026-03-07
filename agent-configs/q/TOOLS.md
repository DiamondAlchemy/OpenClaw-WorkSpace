# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## Workspace Structure
- **Facilities:** `facilities/` (per-folder structure: call-logs, daily-summaries, issues, batches)
- **Scripts:** `scripts/`
- **Data:** `data/`

## Inter-Agent Communication
Use the shared folder: `/Users/m/.openclaw/workspace/shared/`

**To Send:**
- Write to: `/Users/m/.openclaw/workspace/shared/outbox/[recipient]-[timestamp].md`
- Format:
  ```
  # From: Q
  # To: [recipient] (moneypenny, octopussy, Alvie, Christian)
  # Time: [ISO timestamp]

  [Message]
  ```

**To Receive:**
- Check: `/Users/m/.openclaw/workspace/shared/inbox/` for files addressed to `q`.

## Google Drive
- **Data Folder:** https://drive.google.com/drive/folders/14roJ3yl8v0WJaSWczNF1MFg7PaiVg-av
- Use this folder for uploading logs, batch records, and data exports

## Partners
- **Alvie (Diamond):** Primary contact, Telegram 8217045820
- **Christian (Wannabee63):** Partner, Telegram 7437937082
- **MoneyPenny:** Agent orchestrator
- **Octopussy:** Reporter
