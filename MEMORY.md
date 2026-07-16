# MEMORY — Consolidated Knowledge Base

> **Last updated:** 2026-03-22 (manual update — do not overwrite with stale consolidation)

---

## System & Configuration

- **Primary AI Model:** `minimax/MiniMax-M2.7-highspeed` (all agents except Towelie)
- **Towelie model:** `minimax/MiniMax-M2.5-highspeed` (dumber, more obedient — intentional for data intake)
- **Fallback:** `google/gemini-2.5-pro`
- **Vision (manifest images):** `summarize` with `--model google/gemini-3.1-pro-preview` + `--prompt` — MiniMax hallucinates manifest data, never use direct vision
- **Provider config:** New `minimax` provider block added to openclaw.json (2026-03-20) with API key in env
- **Backup config:** `openclaw.json.backup-m25-working` — last known good M2.5 config
- **Google Workspace:** gog CLI with multiple clients (moneypenny, octopussy, q, towelie). **Default account: `moneypenny@topsecretworkshops.com` with `--client moneypenny`.** The old default `00qm00qm@gmail.com` is DEAD — disabled by Google 2026-04-06. Always use: `export GOG_ACCOUNT=moneypenny@topsecretworkshops.com` and `--client moneypenny`.
- **Backup:** Daily cron at 6 AM, 7-day retention, `~/Backups/OpenClaw/`
- **Memory consolidation:** `ai_consolidate_memory.py` in workspace root (NOT `consolidate_memory.py` in workspace-shared)
- **Global thinking:** `"thinkingDefault": "high"` — no per-agent override available
- **Control UI token:** `7ef5ed4aabc935e07746daf96d3a562876b516b4a62a8511`

---

## People & Contacts

- **Alvie (Diamond):** Primary operator. Telegram: 8217045820. Email: diamondalchemy@topsecretworkshops.com
- **Christian (Wannabee63):** Partner. Telegram: 7437937082. Email: wannabee63@topsecretworkshops.com
- **Naming:** "Alvie" for direct, "Diamond" for formal/public

---

## Agent Ecosystem (as of 2026-03-22)

| Agent | Role | Workspace | Model |
|-------|------|-----------|-------|
| MoneyPenny | Orchestrator | `workspace/` | M2.7-highspeed |
| Q | Facility ops architect — designs templates, trains scripts with Alvie | `workspace-q/` | M2.7-highspeed |
| Towelie | Cannascend data intake (PRODUCTION READY) | `workspace-cannascend/` | M2.5-highspeed |
| Octopussy | Monthly KPI reporter for Christian | `workspace-octopussy/` | M2.7-highspeed |
| Felix | Telegram scraping | `workspace-shared/` | M2.7-highspeed |

- **Goldfinger (cryptobot):** Alvie's separate side project at `workspace-goldfinger/`. NOT part of the facility system. Do not reference or manage.
- **Subagent permissions:** `agents.{id}.subagents.allowAgents: ["*"]` (inside agent definition, NOT "commands" section)

---

## Facility Agent System (LIVE — 2026-03-20)

**Template:** `~/.openclaw/facility-agent-template/`
- Deploy: `python3 deploy_facility_agent.py <config.json>`
- 36 golden rules, trained intake script, parameterized workspace files
- Scripts folder: golden-rules.md, intake.md, extraction.md (pending), post-extraction.md (pending)

**Shared facilities folder:** `workspace-shared/facilities/` — universal source of truth for facility config

**Deployed agents:**
- **Towelie (Cannascend)** — first production deploy (2026-03-20, production ready 2026-03-22)
  - Bot: `@CannascendBot`
  - Sheet: "KPI for Cannascend Extraction Operations" (ID: `1VES7AKgtlJ0KGBQEewlHR69F28ra4uXOvLjzxFgBAx4`)
  - gog account: `therealdiamondalchemy@gmail.com` (client: towelie)
  - Telegram group: -1003892536539 (topics: General=1, Intake=12, Extraction=13, Post Extraction=14)
  - Leads: Mark (Intake, 8222701247), Rob (Extraction, 8776456057), Evan (Post-Extraction, 5611416903)
  - Notifies Diamond via DM after each intake

**Q's role:** Architect — designs templates, trains scripts. Does NOT collect production data. Test environment: Facility 01 (FW Green Investments, sheet `1q981lG9UFCPDf4zGeT9BKwcNkbGaYGok0DW1a1VERog`)

---

## Workspace Cleanup (2026-03-19/20)

All agent workspaces audited and cleaned:
- **Q:** SOUL rewritten (architect role, execution mode), removed duplicate files, personality backed up at `SOUL.md.personality-backup`
- **Octopussy:** Consolidated 3 duplicate spec files into 1, fixed model selection (M2.5 Pro fallback), removed stale files
- **Felix:** Fixed path typos (`workplace-shared` → `workspace-shared`), real TOOLS.md, cleaned AGENTS.md
- **MoneyPenny:** Removed Goldfinger/crypto references, updated agent roles, updated facility system status
- **All:** Removed cross-agent Goldfinger/crypto references (Alvie's side project stays separate)

---

## Operational Protocols

- **Startup:** Read SOUL.md → USER.md → memory/YYYY-MM-DD.md (today + yesterday)
- **File verification:** After any write/edit, verify with ls/read/cat
- **Naming:** "Alvie" direct, "Diamond" formal
- **Reports to Christian:** Only when explicitly requested by Alvie

---

## Bugs & Fixes (with lessons)

> Format: What broke · Why · What changed · Watch for

- **RESTORE.md silent write failure (2026-03-04):** Write command didn't create the file. No verification step existed. Added mandatory ls/read verification after every write to SOUL.md. **Watch for:** Any file operation that reports success without verification.

- **Telegram routing crossed (2026-03-06):** Octopussy answered in MoneyPenny's chat. Bot tokens weren't bound to correct agents. Fixed with explicit agent-to-bot bindings in openclaw.json. **Watch for:** Config patches that lose agent bindings.

- **gog OAuth blocked (ongoing):** `unauthorized_client` error. Default OAuth client in GCP testing mode blocks workspace accounts. Created new client in moneypenny-489014 project. **Needs:** Add `moneypenny@topsecretworkshops.com` as Test User in GCP OAuth consent screen. **Watch for:** This blocks Gmail/Drive heartbeat checks.

- **MiniMax M2.7 model ID (2026-03-20):** `minimax-portal/MiniMax-M2.7-highspeed` rejected as unknown. Old portal provider didn't have M2.7 registered. Fixed by adding new `minimax` provider block to openclaw.json with separate API key. **Watch for:** New MiniMax models may need to be added to the provider block.

- **MiniMax vision hallucination (2026-03-19):** MiniMax fabricated METRC numbers, strains, and weights when reading manifest images directly. Moved to `summarize` with Gemini 3.1 Pro for image extraction. **Lesson:** Never trust MiniMax for manifest vision. Always use summarize + Gemini.

- **Q cross-facility contamination (2026-03-19):** When Q managed multiple facilities, shared memory caused data from one facility to bleed into another. Built facility agent template system — each facility gets isolated workspace with no shared memory. **Lesson:** Per-facility isolation is non-negotiable.

- **Towelie M2.7 too creative (2026-03-22):** M2.7 made jokes, printed reasoning, improvised instead of following rules. Downgraded Towelie to M2.5-highspeed. Dumber but more obedient — exactly what a data intake agent needs. **Lesson:** Smarter models aren't always better for execution-focused agents.

- **Memory consolidation overwrites manual updates (2026-03-22):** `ai_consolidate_memory.py` runs nightly and regenerates MEMORY.md from daily logs, overwriting manual updates with stale data. **Watch for:** Any manual MEMORY.md edit may be lost on next consolidation run. Consider excluding manually-updated sections or adding a `# DO NOT CONSOLIDATE BELOW THIS LINE` marker.

- **Telegram groupPolicy="open" accepted risk (2026-03-23, re-reviewed 2026-04-23):** Security audit flags groupPolicy="open" as a risk. However, setting groupPolicy="allowlist" breaks group communications — Telegram bots receive messages at the group level, not user level, so we can't simply allowlist specific groups. Workaround: groupPolicy="open" + groupAllowFrom with authorized user IDs per account filters who can trigger the bot within any group. This is an accepted trade-off for functional group comms. **Watch for:** Periodic review as team/group structure evolves.

---

## Claude MCP Bridge (2026-05-13)

- **Method:** Claude Desktop → freema/openclaw-mcp (v1.4.1, global npm) → stdio → local Gateway
- **Config:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Gateway:** `chatCompletions` enabled, `http://127.0.0.1:18789`
- **Token:** `9030fa143b4493404bee0dce54cf3de5afe818003651db26`
- **Default route:** Claude → openclaw_chat → Gateway → MoneyPenny
- **Agent targeting:** Not yet configured (would need `OPENCLAW_INSTANCES` env var for per-agent routing)
- **Also in Claude:** TradingView, Hyperliquid, Funding Rates MCPs (Goldfinger/crypto, separate from facility)

## KPI-App MCP Reporting Path (2026-05-30)

- Diamond's engineering Claude briefed the OpenClaw fleet that the KPI-app MCP is the approved facility reporting surface.
- KPI-app MCP is read-only and routes through the KPI app's auth, facility scoping, and audit logging.
- Expected tools include `kpi_whoami`, `get_cost_summary`, `get_dashboard`, `get_process_stats`, and `list_manifests`; more tools are expected later.
- Scaffold/route test location on Diamond's machine: `~/dev/kpi-mcp`.
- Bridge is coming via HTTP, named cloudflared tunnel, and API key, following the Hermes bridge pattern.
- Agents should answer cost, yield, throughput, manifest, and dashboard questions through KPI-app MCP when available, not by CSV exports or direct database access.
- Raw read-only Postgres MCP exists but bypasses app scoping/audit and is Diamond-only. Agents should not request, expect, or use raw DB/SQL access for reporting.

## Pending / Open Items

- **gog OAuth re-auth:** Needs `moneypenny@topsecretworkshops.com` added as Test User in GCP OAuth consent screen
- **Facility agent scripts:** Extraction + post-extraction scripts pending Alvie's input (Q will help design)
- **Memory consolidation conflict:** Nightly cron overwrites manual MEMORY.md updates — needs a solution
- **Voice-call (future):** Alvie wants to set up voice calling via Twilio/Plivo — call MoneyPenny and talk to her verbally. Needs telephony provider setup. Not urgent but flag for near-future implementation.

## Hermes Role/Lane Update — 2026-05-07

Alvie clarified MoneyPenny's current lane.

- Original role: OpenClaw orchestrator.
- Current practical role: alert messenger / breakage notifier.
- Hermes is now the chief-of-staff / director-of-operations layer above OpenClaw.
- MoneyPenny should surface alerts, failures, breakage, and important status signals.
- MoneyPenny should not act as the primary orchestrator over all agents unless Alvie explicitly reassigns that role.
- Any alert or claim should be backed by live files, logs, sessions, or command output so Hermes can verify before reporting to Alvie.

## Promoted From Short-Term Memory (2026-07-16)

<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:14:14 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): **Daily backup Drive upload has been silently failing for ~5+ days.** [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10.md:14-14]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:16:16 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): `cron 842c9d88-fdf2-4b82-90ef-c72d01a6f455` ("Daily agent backup", 3:00 AM CT) keeps writing four zips to `~/Desktop/TopSecretBackups/` but the `gog drive upload` step consistently fails because the unattended cron hits a macOS keychain permission prompt no human is present to dismiss: [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10.md:16-16]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:29:31 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): `date` → today is `2026-07-10`; `cron list` → backup job still enabled, lastRunStatus "ok" (cron fired; upload failed); `heartbeat-state.json` → last write Jul 8, lastChecks.email/drive timestamps stale at 1783498016 (~2026-07-05 06:46) [score=0.844 recalls=0 avg=0.620 source=memory/2026-07-10.md:29-31]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:4:6 -->
- Session state: Webchat session `agent:main:main` started 2026-06-27 09:58 CDT. For ~13 days it has only received pasted text reading `[OpenClaw heartbeat poll]` — never a real heartbeat-channel event with `channel: heartbeat` in its inbound metadata.; Runtime responds to `exec`/`cron`/`gateway` (verified Fri 2026-07-10 15:28 CDT), so the lane is reachable for ad-hoc questions and tasks but my *heartbeat lane* has been silent.; Last prior daily log: `2026-07-05-backup-issue.md`. No `2026-07-08`, `2026-07-09`, or `2026-07-10` log entries existed before this one. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:4-6]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:19:21 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): read token: keyring connection timed out after 30s while reading keyring item (macOS Keychain may be waiting for a permission prompt; run `gog auth list` from a terminal and click "Always Allow" when prompted) [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:19-21]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:24:24 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): Consequence: local zips exist on disk but Drive has nothing. Local 7-day `find ... -delete` cleanup means anything older than 7 days is **gone** — so this is a partial-failure state that, left alone, will become full data loss. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:24-24]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:26:26 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): The cron's own `lastRunStatus` reports `ok` because the cron *fired*; that doesn't reflect the Drive upload failing inside the script. Do not trust cron status alone for this job. [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:26-26]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:28:28 -->
- Real alert (MoneyPenny lane — per 2026-05-07 Hermes role clarification): Source: `memory/2026-07-05-backup-issue.md`. Verified fresh Fri 2026-07-10 15:28 CDT via: [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:28-28]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:34:37 -->
- What I did NOT do (no explicit approval): Did not patch `openclaw.json`; Did not modify the backup script; Did not restart any cron or the gateway; Did not update `MEMORY.md` (Diamond-only) [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:34-37]
<!-- openclaw-memory-promotion:memory:memory/2026-07-10.md:38:38 -->
- What I did NOT do (no explicit approval): Did not send a Telegram alert (no explicit ask; staying in webchat) [score=0.812 recalls=0 avg=0.620 source=memory/2026-07-10.md:38-38]
