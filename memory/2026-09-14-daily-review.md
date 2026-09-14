# Daily Self-Review — 2026-09-14 (Monday)

- Trigger: Daily Self-Review cron, 08:00 America/Chicago
- Audited: SOUL.md, WORKSPACE.md, IDENTITY.md, AGENTS.md, USER.md, TOOLS.md, HEARTBEAT.md, MEMORY.md (structure only), skills/, live cron list
- Prior review: 2026-08-06 (39-day gap)
- No core files modified.

## MEMORY.md structure
- 153 lines / 10,904 bytes / 13 sections. No duplicate headings, no trailing whitespace, no null bytes, max 1 consecutive blank. Structurally clean.
- One long line: L108 (577 chars, Telegram groupPolicy entry).
- Stale "Last updated: 2026-03-22" header (~6 months).
- SECURITY: two plaintext tokens — L19 Control UI token, L117 Claude MCP Bridge token.
- 4 stale backups at workspace root (backup_20260313 ×3, before-2026-05-07) — flagged in prior reviews, still there.
- "Promoted From Short-Term Memory (2026-09-10)" footer intact but promoted content is cryptic score metadata, low recall value.

## Core file findings
- MODEL DRIFT (all docs): SOUL/WORKSPACE/MEMORY say MiniMax-M2.7-highspeed primary. Live session: google/gemini-flash-latest (fallback zai/glm-5.3-flash); runtime default xai/grok-4.6. 2026-05-29 decision moved to GPT default. Docs never caught up. 3rd+ consecutive review flag.
- AGENTS.md "6,400+ lines" MEMORY.md claim still factually wrong (153 lines). Flagged 2026-07-28 and 2026-08-06.
- TOOLS.md still points to non-existent nano-banana-pro skill path (bundled skills list has no nano-banana-pro; on-disk skill is minimax-image). Flagged 3x.
- TOOLS.md skills list: 13 entries vs 18 on disk (missing brave-browser-agent, browser-auto-plus, google-workspace-operator, minimax-image, twitterwebapi).
- WORKSPACE.md cron table lists 4 jobs; live list has 10 (undocumented: Zorin intl ledger heartbeat, Memory Dreaming Promotion, Moneypenny skills/tools scout, Moneypenny intel briefing, Mo'at quarterly self-review, Mo'at connection sweep).
- WORKSPACE.md backup section: backup_to_drive.sh location listed as uncertain; undocumented scripts/backup_daily.sh also exists.
- MEMORY.md Bugs & Fixes says Telegram groupPolicy="open" accepted risk w/ groupAllowFrom workaround; daily audits since 2026-09-01 report groupPolicy=allowlist. Entry stale vs current config.
- skills/intake uses lowercase `skill.md` (all others use SKILL.md).
- IDENTITY/USER/HEARTBEAT: clean, no conflicts.

## Skills (18 on disk)
brave-browser-agent, browser-auto-plus, chart-image, dashboard, document-pro, fill-docx-template, google-workspace-operator, heartbeat, intake, invoice, kpi, minimax-image, notification-system, pdf-form-filler, report, spreadsheet, twitterwebapi, weekly-report-generator.
- Unused/likely-dead: minimax-image (Mar, superseded by builtin image_generate), intake (no recent use), twitterwebapi (free tier exhausted, no AZT_API_KEY per decisions log), browser-auto-plus + brave-browser-agent (no recorded use since June install).

## Recent failures / lessons
- TOP: Daily agent backup Drive upload failing repeatedly — gog keyring timeout for moneypenny@topsecretworkshops.com on 09-14, 09-13, 09-12, 09-10, 09-08, 09-07, 09-03, 09-01, 07-12. Local-only backups for ~2 months. Unresolved.
- NEW: "Moneypenny skills/tools scout" cron in error state this morning (last run ~06:30, errored; prior days OK).
- Prior review findings (model drift, nano-banana-pro, 6,400+ claim, TOOLS gaps, stale backups) remain open across 3 runs — no owner has actioned them.
- Security audit warnings stable (4 warnings, unchanged since 09-01).
- Daily-log gaps: 08-07→09-03 missing (project-state entries exist); 09-05/09-06 absent.

## Recommendations (no changes made)
1. Fix backup Drive upload: gog re-auth / Keychain "Always Allow" for moneypenny@, or switch upload path. Highest operational risk.
2. Triage skills/tools scout cron error.
3. One approved doc-sync pass: model references (SOUL/WORKSPACE/MEMORY note), AGENTS 6,400 claim, TOOLS nano-banana→minimax-image + 5 missing skills, WORKSPACE cron table + backup section.
4. Archive 4 stale MEMORY.md backups out of root; archive minimax-image/intake/twitterwebapi if confirmed unused.
5. Move the 2 plaintext tokens out of MEMORY.md into secrets.
6. Update stale groupPolicy entry in MEMORY.md (Diamond-maintained; flag only).
