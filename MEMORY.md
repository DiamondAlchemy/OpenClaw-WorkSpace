# MEMORY — Consolidated Knowledge Base

> **Last consolidated:** 2026-03-22 00:00:06
> **Source:** 32 daily logs (2026-03-03-enable-shell to 2026-03-16-security-audit-accepted-risks)
> **Method:** AI-powered consolidation (ai_consolidate_memory.py)

---

## System & Configuration

- **Primary AI Model:** MiniMax M2.5 Highspeed (primary), Gemini 2.5 Flash (fallback)
- **Additional Models Available:** Groq Llama 3.3 70B, OpenAI GPT-4o Mini, Ollama (llama3.2, deepseek-r1, mistral)
- **Google Workspace:** gog CLI configured with service account (money-penny@moneypenny-489014.iam.gserviceaccount.com); Drive folder: `MoneyPenny_Intelligence`
- **Backup:** Daily cron at 6 AM, 7-day retention, stored in `~/Backups/OpenClaw/`
- **Security:** Main agent locked to `workspaceOnly: true`; rate limiting on auth (5 attempts/min); risky web tools disabled for small models
- **Control UI token:** `7ef5ed4aabc935e07746daf96d3a562876b516b4a62a8511`
- **Known Accepted Risks:** `groupPolicy="open"` with elevated tools and filesystem access; `camera.snap`/`screen.record` enabled on Mac mini; recurring Telegram warnings
- **Workspace Structure:**
  - Main: `/Users/m/.openclaw/workspace/`
  - Octopussy: `/Users/m/.openclaw/workspace-octopussy/`
  - Shared: `/Users/m/.openclaw/workspace-shared/`
  - Cryptobot: `/Users/m/.openclaw/workspace-cryptobot/`

---

## People & Contacts

- **Alvie** (diamondalchemy@topsecretworkshops.com) — Primary operator; Telegram ID: 8217045820
- **Christian** (wanabee63@topsecretworkshops.com) — Business partner; Telegram ID: 7437937082
- **Q** — Contact handling Facility Manager / cannabis cultivation data project (CannaLog)
- **Naming Convention:** "Alvie" for personal/direct; "Diamond" for formal/public contexts

---

## Operational Protocols

- **Session Startup:** Read `SOUL.md` → `USER.md` → `IDENTITY.md` → daily memory logs → heartbeat check
- **Heartbeat:** Monitors Gmail (unread), Drive (new files), local Intel drops (`/Users/m/Desktop/MoneyPenny_Intelligence`)
- **Daily Self-Review:** Runs `daily_self_review.py` via cron; scans for file integrity issues, inconsistencies, and operational lessons from past 7 days
- **Inter-Agent Comms:** Telegram group (`-1003789330057`) for Q/Octopussy/MoneyPenny coordination; signed message protocol available
- **Pre-Flight Check:** Not yet implemented (proposed improvement from 2026-03-04 review)
- **No-Repeat Rule:** Do not re-report known/acknowledged failures within 24hrs unless resolution changes

---

## Business Operations (Cannabis/TSW)

- **CEO Data Manager Agent:** Soul file created (`ceo_data_manager_soul.md`); folder structure set up in Drive
  - Handles: Intake, Extraction, Post Processing data collection via structured scripts
  - **Status:** 5 scripts still pending training (scripts.md empty); not yet live
- **Monthly Reporter:** Generates TSW KPI reports; emails to Alvie + Christian; Google Doc output
- **Octopussy Agent:** Facility reporting agent for Christian; workspace-synced from main; MiniMax-only mode

---

## Crypto & Trading

- **Workspace:** `/Users/m/.openclaw/workspace-cryptobot/`
- **Data On Hand:** BTC + ETH 10m OHLCV (Oct 2025–Mar 2026, ~20k candles each); BTC/ETH multiple timeframes (1m–4h)
- **Best Strategy Found:** ICT Bollinger Bands Liquidity Sweep
  - Params: BB std dev 4.0, swing 40 candles
  - ETH (10m): **+1,460%** return, 66% win rate, 9,639 trades
  - BTC (10m): **+893%** return, 62% win rate, 9,775 trades
  - Saved: `workspace-cryptobot/strategies/ICT_BB_Sweep_Optimized.md`
- **Secondary Strategy:** RSI Extreme Reversion (RSI<20 long, RSI>85 short)
- **Pending:** Code ICT BB Sweep into cryptobot; acquire BloFin API keys for live trading
- **Current Market (Mar 11):** BTC ~$70,935, RSI 75.3 (overbought), ETH ~$2,079

---

## Agent Ecosystem

| Agent | Purpose | Model | Workspace |
|-------|---------|-------|-----------|
| MoneyPenny (main) | Primary handler, Alvie's assistant | MiniMax/Gemini | `/workspace/` |
| Octopussy | Christian's facility reporting | MiniMax only | `/workspace-octopussy/` |
| Felix (The Messenger) | Telegram scraping | MiniMax | `/workspace-shared/` |
| Q | Facility Manager data analysis | MiniMax/Gemini 3 Pro | — |
| CEO Data Manager | Cannabis ops data collection | TBD | TBD |

- **Auto-spawn protocol:** Must ask Christian before spawning Gemini subagents
- **Subagent permissions:** Config path is `agents.{id}.subagents.allowAgents: ["*"]` (not in "commands" section)

---

## Bugs & Fixes

- **RESTORE.md missing file:** Agent failed to write file on first attempt; corrected by writing and verifying all future files per new SOUL.md directive
- **SOUL.md write verification:** Added mandatory `ls`/`read` verification step after every file write
- **gog OAuth `unauthorized_client`:** Default OAuth client in testing mode blocked access; workaround: created new client in moneypenny-489014 GCP project with service account auth
- **WhatsApp heartbeat config:** `channels.whatsapp.web` key invalid in current OpenClaw version; removed; heartbeat kept at default ~60s
- **Obsidian skill:** CLI installed but vault not registered; removed config entry (was breaking gateway); files readable directly from vault folder
- **Whisper uninstalled:** `openai-whisper` and `openai-whisper-api` removed as redundant
- **Subagent permission path:** Config for spawning subagents belongs inside agent definition (not "commands" section)
- **Config revert cleanup:** MiniMax traces removed; only MiniMax-M2.5 kept; primary model reverted to MiniMax M2.5 Highspeed

---

## Pending / Open Items

- **gog OAuth re-auth:** New OAuth client created but `moneypenny@topsecretworkshops.com` not yet added as Test User in Google Cloud Console → OAuth consent screen. Heartbeat Gmail/Drive checks blocked until resolved.
- **CEO Data Manager:** Scripts not trained; agent not yet live. Needs: facility details in `facilities.md`, Google Sheet setup for facility-01, script training complete
- **Cryptobot live trading:** ICT BB Sweep strategy needs to be coded into the bot; BloFin API keys needed (Alvie to create on desktop)
- **Projects.md dashboard:** Proposed during 2026-03-04 workflow review; never created. Would provide strategic context at startup
- **Weekly Sit-Rep:** Proposed enhancement to extend startup memory window beyond 48hrs; not implemented
- **Evolving Persona Process:** Proposed daily self-review to flag `SOUL.md` edit suggestions from feedback; not implemented