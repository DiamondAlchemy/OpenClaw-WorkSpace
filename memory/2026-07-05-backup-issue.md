# 2026-07-05 — Daily backup cron issue

## Status: PARTIAL — local zips OK, Drive upload FAILED

Cron `842c9d88-fdf2-4b82-90ef-c72d01a6f455` (Daily agent backup, 3:00 AM CT) ran.

### What worked
All 4 zips written to `~/Desktop/TopSecretBackups/` by 03:04 CT:
- `q_workspace_2026-07-05_0302.zip` (36,720 bytes)
- `octopussy_workspace_2026-07-05_0302.zip` (16,034,055 bytes)
- `shared_2026-07-05_0302.zip` (2,225,087,521 bytes — ~2.1 GB)
- `cannascend_workspace_2026-07-05_0302.zip` (35,177,482 bytes)

### What failed
The script's `gog drive upload ...` step hit a macOS keychain permission prompt that no human was there to click "Always Allow" on. After 30s the gog binary gave up:

```
read token: keyring connection timed out after 30s while reading keyring item
(macOS Keychain may be waiting for a permission prompt; run `gog auth list`
from a terminal and click "Always Allow" when prompted)
```

Setting `GOG_KEYRING_OPEN_TIMEOUT=90` had no effect — gog appears to hardcode the 30s wait regardless of the env var. None of the 4 uploads made it to Drive.

The whole process was also killed by my exec session timeout (120s) before it could give up cleanly, since the zipping alone takes ~3-4 minutes on the shared/ folder.

### This is a recurring problem
Same symptom: local zips keep landing on disk for the past week, but Drive upload has been silently failing because the unattended cron can't satisfy the keychain prompt.

### Fix options for Diamond to consider
1. Run `gog auth list` once interactively and click "Always Allow" so the keychain item is unlocked for future unattended runs.
2. Switch gog to file-based token storage: `GOG_KEYRING_BACKEND=file GOG_KEYRING_PASSWORD=<pw>` and bake that into the script.
3. Add `nohup` + detached logging to the script so the upload step isn't bounded by the cron exec timeout.
4. Have the cron announce the partial-failure state and retry the upload step later in the morning when someone might be at the Mac.

Local backups on disk are NOT automatically retried — the 7-day `find ... -delete` cleanup is still running, so anything older than 7 days is gone.
