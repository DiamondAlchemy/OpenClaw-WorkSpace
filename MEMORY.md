# MEMORY — Consolidated Knowledge Base

> **Last consolidated:** 2026-03-19 00:01:05
> **Source:** 32 daily logs (2026-03-03-enable-shell to 2026-03-16-security-audit-accepted-risks)
> **Method:** AI-powered consolidation (ai_consolidate_memory.py)

---

## System & Configuration

- **Gateway running at:** `ws://127.0.0.1:18789`
- **Control UI:** `http://localhost:18789` (origins: `http://localhost:8080`)
- **Gateway token:** `7ef5ed4aabc935e07746daf96d3a562876b516b4a62a8511`
- **Main workspace:** `/Users/m/.openclaw/workspace`
- **Model (current runtime):** `minimax-portal/MiniMax-M2.5-highspeed` (set 2026-03-05)
- **Startup model priority:** MiniMax → Gemini 3 Pro → Gemini 3 Flash → Gemini 2.5 Pro → Gemini 2.5 Flash → GPT-4o Mini → Groq Llama → Ollama Llama
- **Node commands allowed:** `camera.snap`, `screen.record`, `canvas.snapshot`, `system.notify`, `system.run` — accepted risk (2026-03-04)
- **Memory files location:** `/Users/m/.openclaw/workspace/memory/YYYY-MM-DD.md`
- **Use `memory_search` tool** for long-term recall; do NOT read MEMORY.md directly
- **Backup cron:** daily at 6 AM, keeps 7 days → `~/Backups/OpenClaw/`
- **WhatsApp connected** and active; added to Cannascend OH group in listen-only mode

## People & Contacts

- **Alvie (Diamond):** `diamondalchemy@topsecretworkshops.com`, Telegram ID `8217045820`
  - Real name: Alvie (used in direct comms)
  - Online handle: `diamond_alchemy` / `Diamond` (used in social media/public)
- **Christian (The Partner):** `wanabee63@topsecretworkshops.com`, Telegram ID `7437937082`
- **Q (External Contact):** `diamondalchemist@proton.me` — running the "Facility Manager" cannabis cultivation tracking project with Alvie

## Operational Protocols

- **Session startup sequence:** Read `SOUL.md` → `IDENTITY.md` → `USER.md` → `memory/YYYY-MM-DD.md` (today + yesterday)
- **Write verification rule:** After `write`/`edit`, always run `ls` or `read` to verify file creation (added 2026-03-04 after RESTORE.md failure)
- **Plan-first protocol:** For multi-step tasks, present plan and wait for approval before executing
- **Reporting rule:** Do not send duplicate reports to Christian unless explicitly asked; all reports go to Alvie first
- **Config change rule:** Do not interfere with Alvie's direct `openclaw config` changes; communicate any potential system file modifications clearly
- **Naming convention:** Default to "Alvie" for direct comms; "Diamond" for formal/public contexts

## Business Operations (Cannabis/TSW)

### Monthly Reporter Agent (Octopussy)
- **Bot:** `@Octopussy_openclawbot` (token: `8408646621:AAHYCVgFklp3R_EJudpj6YCoRg-prYcWs1c`)
- **Primary model:** MiniMax M2.5 Highspeed; **Fallback:** Gemini 2.5 Pro
- **Workspace:** `/Users/m/.openclaw/workspace-octopussy`
- **Bind:** Christian's DMs (Telegram `7437937082`) route to Octopussy; Alvie's DMs route to MoneyPenny
- **Auto-spawn rule:** Must ask Christian before spawning Gemini subagents (Gemini doesn't handle spreadsheet data well)

### CEO Data Manager Agent (Planned)
- **SOUL defined:** `workspace/ceo_data_manager_soul.md` — cannabis extraction data collection agent
- **Scope:** 3 departments per facility (Intake, Extraction, Post Processing) → Google Sheets
- **Strict data rules:** Never log unconfirmed data; always read back entry for confirmation; never close session with missing fields
- **Folder structure:** `/facilities/facility-01/` with `call-logs/`, `daily-summaries/`, `issues/`, `batches/` subfolders
- **Supporting files created:** `facilities.md`, `active-runs.md`, `issues.md`, `scripts.md`, `preferences.md`
- **Google Drive folder:** `1jDyfvtXAh6pcX_K2TVhBKBPlEI-JvHYS`
- **Status:** On hold — scripts.md pending training before activation

### TSW Partner Emails
- **Outbound email:** `diamondalchemy@topsecretworkshops.com` → `wanabee63@topsecretworkshops.com` (Christian)

## Crypto & Trading

### CryptoBot Workspace
- **Location:** `/Users/m/.openclaw/workspace-cryptobot`
- **Best strategy found:** ICT Bollinger Bands Liquidity Sweep
  - **BB Std Dev:** 4.0, **Swing LB:** 40
  - **ETH 10m:** +1,460% | 66% win rate | 9,639 trades (bear market period Oct 2025–Mar 2026)
  - **BTC 10m:** +893% | 62% win rate | 9,775 trades
- **Secondary strategy:** RSI Extreme Reversion (RSI<20 long, RSI>85 short)
  - Combined return: +122.6% in bear market
- **Data files saved:** `BTC_10m.csv` (20,531 candles), `ETH_10m_long.csv` (20,531 candles)
- **Pending:** BloFin API keys for live trading; strategy code pending deployment
- **Strategy files:** `workspace-cryptobot/strategies/RSI_extreme_reversion.md`, `ICT_BB_Sweep_Optimized.md`

### Model Arsenal (as of 2026-03-05)
| Provider | Model | Status |
|----------|-------|--------|
| MiniMax | M2.5 Highspeed | Primary |
| Google | Gemini 3 Pro Preview | Active |
| Google | Gemini 3 Flash Preview | Active |
| Google | Gemini 2.5 Pro | Active |
| Google | Gemini 2.5 Flash | Active |
| OpenAI | GPT-4o Mini | Active |
| Groq | Llama 3.3 70B | Active |
| Ollama | Llama 3.2 (local Mac mini) | Active |
| Ollama | DeepSeek R1, Mistral | Pulled |

## Agent Ecosystem

### MoneyPenny (Main Agent)
- **Primary operator:** Alvie (Telegram `8217045820`)
- **Bot:** `@MoneyPenny_openclawbot` (token: `8641071709:AAFKfMvmmsV83aKZDMjHDkmD7Ik_fdQuKas`)

### Octopussy (Monthly Reporter)
- **Primary operator:** Christian (Telegram `7437937082`)
- **Tasks:** Monthly KPI reports, data extraction from Google Sheets → Google Docs → email to partners

### Q (Research/Trading)
- **Workspace:** `/Users/m/.openclaw/workspace-q`
- **Model:** MiniMax M2.5 Highspeed; **Fallback:** Gemini 3 Pro-preview

### The Messenger (Felix)
- **Role:** Specialized Telegram scraping agent
- **Bot:** New separate bot token
- **Workspace:** `/Users/m/.openclaw/workspace-shared`
- **Avatar:** Generated via `nano-banana-pro` (Gemini Pro Image)

### Subagent Permissions
- Config path for allowing subagent spawning: `"subagents": { "allowAgents": ["*"] }` inside each agent definition
- **Do NOT put in top-level `commands` section** — breaks the gateway

## Bugs & Fixes

- **RESTORE.md not created:** `write` command silently failed; added mandatory verification step after all write operations (2026-03-04)
- **MiniMax API endpoint:** `https://api.minimax.io/v1` (not `/v1/models`); API type: `openai-chat` (2026-03-05)
- **Config revert issue:** MiniMax was accidentally removed; restored via programmatic cleanup of `openclaw.json` (2026-03-05)
- **WhatsApp config:** `channels.whatsapp.web` key not supported in OpenClaw version; removed; heartbeat stays at default 60s (2026-03-06)
- **Octopussy routing:** DM routing to Octopussy failed repeatedly; fixed by adding `telegram.dmPolicy: allowlist` and explicit agent bindings in config (2026-03-06)
- **Telegram group access:** Per-account `groupPolicy: allowlist` was incorrectly blocking group participation; changed all to `groupPolicy: open` with `groupAllowFrom` controlling access (2026-03-09)
- **Groq security:** Disabled web tools (`web_search`, `web_fetch`, `browser`) for Groq models (≤300B params) due to security concerns (2026-03-07)
- **gog OAuth:** Tokens failing `unauthorized_client`; default OAuth client in "testing" mode; created new client in `moneypenny-489014` project but also blocked; solution: add `moneypenny@topsecretworkshops.com` as Test User in GCP OAuth consent screen (ongoing, not yet resolved as of 2026-03-10)

## Pending / Open Items

- **gog OAuth re-authentication:** Google Workspace auth (`moneypenny@topsecretworkshops.com`) still blocked with `unauthorized_client` error — needs Test User added to GCP OAuth consent screen
- **CEO Data Manager activation:** Scripts not trained in `scripts.md`; cannot accept department lead data until training is complete
- **Crypto bot live trading:** BloFin API keys not yet created; strategy code not yet deployed
- **Google Sheets/Labs integration:** Christian's facilities Google Sheet structure not yet built; data collection workflows pending