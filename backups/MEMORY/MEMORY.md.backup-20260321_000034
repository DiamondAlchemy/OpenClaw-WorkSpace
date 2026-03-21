# MEMORY — Consolidated Knowledge Base

> **Last consolidated:** 2026-03-20 00:00:19
> **Source:** 32 daily logs (2026-03-03-enable-shell to 2026-03-16-security-audit-accepted-risks)
> **Method:** AI-powered consolidation (ai_consolidate_memory.py)

---

## System & Configuration

### Core Files & Identity
- **Avatar:** `avatars/avatar.jpg` (added 2026-03-04 by Alvie)
- **Persona:** Money Penny — witty, professional, direct
- **Naming Convention:** Alvie (real name) for personal context; Diamond (social media handle `diamond_alchemy`) for formal/public-facing situations

### Verified File Operations Protocol [2026-03-04]
- **Rule Added to SOUL.md:** "Verify All Write Operations" — after any `write` or `edit` operation, perform `ls`, `read`, or `cat` to confirm success
- **Trigger:** RESTORE.md failed silently during a write operation — this caused a process failure

### AI Model Configuration [2026-03-05]
- **Primary:** MiniMax-M2.5-Highspeed (OAuth)
- **Fallbacks:** Gemini 3 Pro-preview → Gemini 3 Flash-preview → Gemini 2.5 Pro → Gemini 2.5 Flash → GPT-4o Mini → Groq Llama 3.3 → Ollama Llama
- **Note:** MiniMax removed entirely 2026-03-05 due to persistent HTTP 404 errors with API endpoint
- **Model IDs Verified:** `google/gemini-2.5-flash`, `minimax-portal/MiniMax-M2.5-highspeed`

### External Integrations
- **gog (Google Workspace):** Service account auth configured — `money-penny@moneypenny-489014.iam.gserviceaccount.com` (JSON key at workspace)
- **OAuth Issue (PERSISTENT):** `unauthorized_client` error — GCP OAuth client in testing mode; needs `moneypenny@topsecretworkshops.com` added as Test User in Google Cloud Console → OAuth consent screen
- **Google APIs Enabled:** Drive API, Gmail API, Google Docs API, Google Slides API
- **WhatsApp:** Active and connected to "Cannascend OH" group (listen-only)
- **Telegram Desktop:** Installed via `brew install telegram`

### Agent Workspaces
- **Main (`main`):** `/Users/m/.openclaw/workspace` — workspaceOnly: true (locked down)
- **Octopussy:** `/Users/m/.openclaw/workspace-octopussy` — Christian's facility reporting agent
- **Shared:** `/Users/m/.openclaw/workspace-shared/` — for inter-agent collaboration
- **Cryptobot:** `/Users/m/.openclaw/workspace-cryptobot/`

### Telegram Routing
| Bot | Agent | Bound To |
|-----|-------|----------|
| @MoneyPenny_openclawbot | MoneyPenny | Alvie (8217045820), Christian (7437937082) |
| @Octopussy_openclawbot | Octopussy | Alvie (8217045820) |
| @Q_topsecret_workshops_bot | Q | Alvie (8217045820), Christian (7437937082) |
| @Octopussy_reporter_bot | Octopussy | Christian (7437937082) |
| @Felix_topsecret_bot | Felix | Alvie (8217045820), Christian (7437937082) |

### Security Configuration
- **Rate Limiting:** 5 attempts per minute (auth)
- **Dangerous Tools (camera.snap, screen.record):** Enabled intentionally — gateway restricted to local/tailnet
- **Web Tools (web_search, web_fetch, browser):** Disabled for small models (≤300B params) — Groq, Ollama
- **Control UI Origins:** Added `http://localhost:8080`
- **groupPolicy:** Per-account set to "open"; top-level `allowFrom` controls access
- **⚠️ Accepted Risks (do not flag):** Security audit flags for open groupPolicy with elevated tools, runtime/filesystem exposure, and Telegram group warnings — reviewed and accepted as acceptable risks. `groupAllowFrom` lists provide actual access control. Plugins (lossless-claw) flagged for potential exfiltration pattern — reviewed and accepted. This is intentional multi-user setup, not hostile multi-tenant.

---

## People & Contacts

| Name | Email | Telegram ID | Role |
|------|-------|-------------|------|
| Alvie | diamondalchemy@topsecretworkshops.com | 8217045820 | Primary operator |
| Christian | wanabee63@topsecretworkshops.com | 7437937082 | Business partner |

- **Service Account:** money-penny@moneypenny-489014.iam.gserviceaccount.com

---

## Operational Protocols

### Session Startup Sequence
1. Read `SOUL.md` → Identity, personality, boundaries
2. Read `USER.md` → Operative profile
3. Read `projects.md` → Mission briefing (high-level objectives)
4. Read `memory/YYYY-MM-DD.md` → Recent field logs (last 24-48 hours)
5. **Forbidden:** Do not read `MEMORY.md` directly — use `memory_search` tool

### Heartbeat Protocol (HEARTBEAT.md)
- **Email:** Check Gmail for unread messages (`is:unread in:inbox`)
- **Drive:** Check Google Drive for new files (`trashed=false`)
- **Local Intel:** Scan `/Users/m/Desktop/MoneyPenny_Intelligence` for recent drops (`find -mmin -180`)

### Backup System
- **Script:** `/Users/m/.openclaw/workspace/scripts/backup_daily.sh`
- **Schedule:** Daily at 6 AM
- **Retention:** 7 days
- **Location:** `~/Backups/OpenClaw/`
- **Config Backup:** `~/Desktop/openclaw_config_[date].json`

### Daily Self-Review
- **Script:** `daily_self_review.py` (cron job)
- **Checks:** Core files (`SOUL.md`, `IDENTITY.md`, `USER.md`, `AGENTS.md`, `MEMORY.md`), skills directory, memory logs (last 7 days for lessons)
- **Enhanced [2026-03-04]:** Now scans recent memory for keywords (mistake, error, lesson learned)

### Inter-Agent Communication
- **Telegram Group:** -1003789330057 (open for agent comms)
- **Protocol:** Agents reach MoneyPenny directly via Telegram DM

---

## Business Operations (Cannabis/TSW)

### TSW Monthly Report Automation [2026-03-05]
- **Process:** Subagent extracts KPI data from Google Sheets → Creates Google Doc → Sends email to both partners
- **Email Recipients:** diamondalchemy@topsecretworkshops.com, wanabee63@topsecretworkshops.com
- **Doc Created:** "TSW Monthly Report - March 2026"

### CEO Data Manager Agent (Concept) [2026-03-05]
- **Purpose:** Cannabis extraction data collection — collects run log data from department leads
- **SOUL File:** `/Users/m/.openclaw/workspace/ceo_data_manager_soul.md`
- **Three Departments:** Intake, Extraction, Post Processing
- **Batch ID System:** Ties all three departments across run lifecycle
- **Facility Structure:** Independent per facility — `/facilities/[facility]/` with `google-sheet-link.md`, `call-logs/`, `daily-summaries/`, `issues/`, `batches/`
- **Google Drive Folder:** https://drive.google.com/drive/folders/1jDyfvtXAh6pcX_K2TVhBKBPlEI-JvHYS
- **Status:** SOUL written; supporting files created; **scripts.md pending training**

### Escalation Protocol
| Level | Trigger | Action |
|-------|---------|--------|
| Low | Minor self-corrected deviation | Log in session notes |
| Medium | Unresolved issue, unusual yield | Log + notify owner at next opportunity |
| High | Run stopped, equipment down | Notify owner immediately |
| Critical | Safety issue, compliance concern | Stop session, contact owner before anything |

---

## Crypto & Trading

### Data Collected
- **BTC 10m:** 20,531 candles (Oct 2025 – Mar 2026) — $10k starting balance backtested
- **ETH 10m:** 20,531 candles (Oct 2025 – Mar 2026)
- **BTC 1m/3m/5m/15m:** Received 2026-03-11 (shorter timeframes)
- **Location:** `/Users/m/.openclaw/workspace-cryptobot/data/`

### Best Strategy: ICT BB Sweep [2026-03-11]
**Entry:** Price sweeps previous swing high/low, then closes back inside Bollinger Bands
**Stop Loss:** Just outside swept level
**Take Profit:** TP1 = Middle BB, TP2 = Outer BB

**Optimal Parameters:** BB Std Dev 4.0, Swing LB 40

| Timeframe | ETH Return | Win Rate | Trades |
|-----------|------------|----------|--------|
| 10m | **+1,460%** | 66% | 9,639 |
| 1h | +700% | — | — |
| 4h | +384% | — | — |

| Timeframe | BTC Return | Win Rate | Trades |
|-----------|------------|----------|--------|
| 10m | **+893%** | 62% | 9,775 |

**Note:** Bear market period (BTC dropped 35%, $108k → $70k). Shorting with RSI > 85 was more profitable than longing.

### RSI Extreme Reversion (Secondary)
- **LONG:** RSI < 20 → Exit RSI > 50
- **SHORT:** RSI > 85 → Exit RSI < 55
- **Result:** +122.6% combined (697 trades, bear market)

### Open Items
- **BloFin API Keys:** Pending — Alvie needs to create on desktop
- **Strategy Files:** `workspace-cryptobot/strategies/`

---

## Agent Ecosystem

| Agent | Purpose | Model | Workspace | Notes |
|-------|---------|-------|-----------|-------|
| MoneyPenny | Main handler, operations | MiniMax/Gemini Flash | `/workspace` | Locked down (workspaceOnly) |
| Octopussy | Facility reporting | MiniMax + Gemini 2.5 Pro | `/workspace-octopussy` | Christian's agent |
| Q | Crypto operations | MiniMax + Gemini 3 Pro | — | Alvie's crypto agent |
| The Messenger (Felix) | Telegram scraping | — | `/workspace-shared/` | Raven avatar generated |

### Subagent Permissions
- **Config Path:** Inside each agent definition: `"subagents": { "allowAgents": ["*"] }`
- **Auto-spawn Protocol:** Ask Christian before spawning Gemini subagents (Gemini doesn't handle spreadsheet data well)

---

## Bugs & Fixes

| Date | Issue | Resolution |
|------|-------|------------|
| 2026-03-04 | RESTORE.md missing after write (silent failure) | Added verification step to SOUL.md |
| 2026-03-04 | SOUL.md "Vibe" section had overlapping concepts | Consolidated redundant items |
| 2026-03-04 | IDENTITY.md/Diamond naming inconsistency | Standardized to Alvie (real), Diamond (formal) |
| 2026-03-05 | MiniMax HTTP 404 (wrong API endpoint) | Removed MiniMax entirely |
| 2026-03-05 | WhatsApp web config key unsupported | Removed; heartbeat stays at default ~60s |
| 2026-03-05 | Obsidian vault not registered in config | Removed config entry; direct folder access maintained |
| 2026-03-06 | Octopussy agent not in config (reverted) | Re-added with correct Telegram binding |
| 2026-03-06 | Telegram routing crossed (Octopussy answering in MoneyPenny chat) | DMs routed correctly to each bot |
| 2026-03-07 | Small models (Groq) with web tools + no sandbox | Disabled web_search, web_fetch, browser for ≤300B models |
| 2026-03-07 | Subagent permissions config in wrong section | Correct path: inside agent definition, not "commands" section |

---

## Pending / Open Items

| Item | Status | Notes |
|------|--------|-------|
| **gog OAuth re-authentication** | **ACTIVE BLOCKER** | `unauthorized_client` — GCP OAuth client in testing mode. Add `moneypenny@topsecretworkshops.com` as Test User in Google Cloud Console → OAuth consent screen |
| **CEO Data Manager scripts.md** | Pending training | 5 scripts (Intake, Extraction Start/End, Post Processing, Issue Report) not yet written |
| **BloFin API keys** | Pending | Alvie needs to create on desktop — needed for live trading |
| **projects.md** | Never created | High-level mission dashboard was proposed but never implemented |
| **Weekly Sit-Rep** | Proposed, not implemented | End-of-week summary to supplement daily logs |
| **Memory consolidation** | Completed 2026-03-20 | This document — first full memory consolidation |