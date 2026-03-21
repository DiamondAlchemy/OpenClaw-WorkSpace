# MEMORY — Consolidated Knowledge Base

> **Last consolidated:** 2026-03-21 00:00:05
> **Source:** 32 daily logs (2026-03-03-enable-shell to 2026-03-16-security-audit-accepted-risks)
> **Method:** AI-powered consolidation (ai_consolidate_memory.py)

---

## People & Contacts

- **Alvie (Diamond / @diamond_alchemy):** Primary operator. Telegram ID: `8217045820`. Email: `diamondalchemy@topsecretworkshops.com`
- **Christian (Wanabee):** Partner. Telegram ID: `7437937082`. Email: `wanabee63@topsecretworkshops.com`
- **Q:** Contact in cannabis/Facility Manager project. Active Telegram conversation.

## Agent Ecosystem

- **MoneyPenny (main):** Primary agent. Telegram bot: `@MoneyPenny_openclawbot`. Workspace: `/Users/m/.openclaw/workspace/`
- **Octopussy:** Facility reporting agent for Christian. Bot token: `8408646621:AAHYCVgFklp3R_EJudpj6YCoRg-prYcWs1c`. Workspace: `/Users/m/.openclaw/workspace-octopussy/`
- **Q Agent:** Trading/crypto agent. Workspace: `/Users/m/.openclaw/workspace-q/`
- **The Messenger (Felix):** Telegram scraping agent. Bot token configured separately.
- **All sub-agents:** Set with `workspaceOnly: true` and `subagents.allowAgents: ["*"]`

## System & Configuration

- **Gateway Auth Token:** `7ef5ed4aabc935e07746daf96d3a562876b516b4a62a8511`
- **WhatsApp:** Connected via OpenClaw plugin
- **Backup System:** `/Users/m/.openclaw/workspace/scripts/backup_daily.sh` — daily cron at 6 AM, 7-day retention
- **gog Auth:** OAuth issues (`unauthorized_client`). New client `moneypenny` created. Needs user added to OAuth consent screen.
- **Telegram Groups:** Group ID `-1003789330057` (active)
- **Desktop Restore Guide:** `/Users/m/Desktop/MONEYPENNY_RESTORE.txt`

## Crypto & Trading

- **WINNING STRATEGY: ICT Bollinger Bands Liquidity Sweep**
  - Entry: Price sweeps previous swing high/low, closes back inside BB
  - SL: Just outside swept level
  - TP1: Middle BB, TP2: Outer BB
  - Params: BB Std Dev 4.0, Period 20, Swing LB 40
  - **10m Backtest Results (Oct 2025 - Mar 2026, bear market):**
    - ETH: **+1,460%** | 66% WR | 9,639 trades
    - BTC: **+893%** | 62% WR | 9,775 trades
  - Saved to: `workspace-cryptobot/strategies/BEST_STRATEGY_FINAL.md`

- **Backup Strategies:**
  - RSI 30/50 (oversold entry): BTC +0.57%, ETH +0.57%
  - RSI Long/Short (85/55): Beats buy-hold by 17%
  - Shorting RSI>85 more profitable than longing in bear markets

- **Data Files:**
  - `BTC_10m.csv`: 20,531 candles
  - `ETH_10m_long.csv`: 20,531 candles
  - All in `workspace-cryptobot/data/`

- **Pending:** Code the ICT BB Sweep strategy into cryptobot; BloFin API keys (desktop creation pending)

## Business Operations (Cannabis/TSW)

- **CEO Data Manager Agent:** Partially built. SOUL saved to `ceo_data_manager_soul.md`
  - Purpose: Collect run log data from 3 departments (Intake, Extraction, Post Processing)
  - Strict data entry rules, caller verification, escalation protocol
  - Folder structure: `facilities/facility-01/` with subfolders for call-logs, daily-summaries, issues, batches
  - Google Drive folder: `1jDyfvtXAh6pcX_K2TVhBKBPlEI-JvHYS`
  - **Status:** Scripts pending training, Google Sheet pending setup for facility-01

- **Octopussy Workflow:** Uses MiniMax only (Gemini fails on spreadsheet data). Config: MiniMax primary + Gemini 2.5 Pro fallback.

- **Monthly Reporter:** Tested, populates Google Docs with KPI data from Sheets, sends emails to both partners.

## Operational Protocols

- **Startup Sequence:** Read SOUL.md → USER.md → projects.md (if exists) → memory/YYYY-MM-DD.md (today + yesterday)
- **File Verification Rule (added 2026-03-04):** After any `write` or `edit`, always verify with `ls`, `read`, or `cat` before reporting success.
- **Naming Convention:** Use "Alvie" for direct interactions, "Diamond" for formal/public contexts.
- **Heartbeat Protocol:** Check Gmail (unread), Drive (recent files), Local intel drops (modified <3hrs).
- **Reports to Christian:** Send only when explicitly requested by Alvie.

## Bugs & Fixes

- **Write verification failure (2026-03-04):** RESTORE.md failed to write silently. Added verification step to SOUL.md.
- **Config revert issues:** Octopussy agent config kept getting lost during MiniMax diagnostics. Fixed by proper programmatic cleanup.
- **Telegram routing:** Octopussy initially answered in MoneyPenny's chat. Fixed by binding correct bot token to correct agent.
- **WhatsApp heartbeat:** `channels.whatsapp.web` key not supported in this OpenClaw version. Removed; using default ~60 sec.
- **gog OAuth:** Default client in "testing" mode blocks workspace accounts. Created new client in moneypenny-489014 project — needs test user added.
- **Anthropic API:** Credit balance too low. Cannot use Claude via API.

## Pending / Open Items

- **gog OAuth re-authentication:** Blocked. Needs `moneypenny@topsecretworkshops.com` added as Test User in GCP OAuth consent screen.
- **CEO Data Manager:** Scripts not trained, facility-01 Google Sheet not created, department leads not onboarded.
- **Cryptobot strategy coding:** ICT BB Sweep needs to be coded into executable bot.
- **projects.md:** Never created. Protocol says to read it, but file doesn't exist — should be built as mission dashboard.
- **Weekly Sit-Rep:** Proposed enhancement to startup sequence — not yet implemented.