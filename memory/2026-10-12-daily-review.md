# Daily Self-Review — 2026-10-12

Ran 08:00 CDT via gateway cron `71fd569d-7940-415c-9f58-1ac499e3bd83`. Read-only: SOUL.md, WORKSPACE.md, IDENTITY.md, AGENTS.md, TOOLS.md, MEMORY.md structure, skills/, vault, crontab, local backup zips. No core files changed.

## Coverage note
- No `memory/2026-10-12.md` yet (normal at 08:00; backup cron writes the 03:00 log).
- No `memory/2026-10-11-daily-review.md` (self-review missed yesterday).
- No `memory/2026-10-09*` (still missing; first noted 2026-10-10).
- `vault/project-state.md` last updated 2026-10-11 09:00 (security audit + backup). `vault/decisions-log.md` last entry 2026-06-24.

## Live vs docs

| Source | Model identity |
|---|---|
| This cron runtime | `xai/grok-4.6` (injected) |
| `session_status` on `current` (webchat main) | `google/gemini-flash-latest`; fallbacks `zai/glm-5.3-flash`, `google/gemini-flash-latest` |
| SOUL / WORKSPACE / MEMORY | MiniMax M2.7-highspeed primary; MiniMax cannot see images; Gemini fallback |

Gateway: OpenClaw `2026.7.1-beta.2`, up ~4h this boot / system 3d.

## MEMORY.md structure (not full load)
- 153 lines / 11,135 bytes. 1 H1, 12 H2, 0 H3.
- Header still says last updated **2026-03-22**. Promotion footer dated **2026-10-06**, recycling 2026-09-14 backup-failure text.
- No CRLF, no empty/duplicate headings, no trailing-space hits.
- Two plaintext tokens still present (Control UI token L19; Claude MCP gateway token L117). Do not reprint.
- Four stale root backups remain: `MEMORY.md.backup_20260313`, two `_20260313_0817*`, `MEMORY.md.before-2026-05-07-hermes-role-lane-update`.

## Skills directory (`workspace/skills/`) — 18 dirs
brave-browser-agent, browser-auto-plus, chart-image, dashboard, document-pro, fill-docx-template, google-workspace-operator, heartbeat, intake, invoice, kpi, minimax-image, notification-system, pdf-form-filler, report, spreadsheet, twitterwebapi, weekly-report-generator.

- **intake** still `skill.md` not `SKILL.md` (only lowercase in the set).
- **minimax-image** last touched Mar 2026; **nano-banana-pro** still documented in TOOLS.md and does not exist in workspace or bundled `/opt/homebrew/lib/node_modules/openclaw/skills`.
- Overlaps: brave-browser-agent vs browser-auto-plus; twitterwebapi vs bundled xurl.
- Little evidence of use: report, dashboard, notification-system, weekly-report-generator, heartbeat (skill vs `HEARTBEAT.md`).

## Repeat findings (unchanged since ~2026-07-28 / daily since Sep)

1. **Model-identity drift.** Docs MiniMax-M2.7 vs live grok-4.6 / gemini-flash-latest / glm-5.3-flash.
2. **AGENTS.md "6,400+ lines" MEMORY.md claim is false** (153 lines / ~11KB).
3. **TOOLS.md nano-banana-pro does not exist.**
4. **TOOLS.md vs AGENTS.md web_search:** TOOLS says built-in is broken, use `scripts/web_search.py` (symlink to `~/.openclaw/tools/web_search.py`, exists). AGENTS says use web search normally (local SearXNG).
5. **intake `skill.md` casing.**
6. **WORKSPACE.md §5 cron table overstates gateway jobs.** This agent's visible gateway cron list = this self-review only. Security audit / GitHub sync / 03:00 agent backup still fire (local 10-12 zips exist) but are not this-agent gateway jobs and are not documented as crontab/launchd.
7. **WORKSPACE.md §6 backup_agents.sh path wrong:** docs say `workspace-shared/`; actual `/Users/m/.openclaw/workspace/scripts/backup_agents.sh`. `backup_to_drive.sh` is in workspace root (exists).
8. **TOP operational risk — offsite backup auth broken since ~2026-07-12.** Local 2026-10-12_0300 zips on Desktop/TopSecretBackups: Q 38K, Octopussy 15M, shared 478M, Cannascend 34M. `zip -T` OK on Q + Cannascend this run. Drive upload still gog keyring timeout (`moneypenny@topsecretworkshops.com`). 10-11 backup exited 0 (no SIGKILL) but offsite still failed.
9. **SOUL.md mandates append to `decisions-log.md` after significant decisions** — file untouched since 2026-06-24.
10. **Hermes lane vs SOUL:** MEMORY.md 2026-05-07 says MoneyPenny is alert messenger / Hermes is chief of staff. SOUL.md still frames MoneyPenny as MI6 handler/orchestrator.
11. **MEMORY.md Telegram groupPolicy lesson is stale:** MEMORY still describes accepted `groupPolicy=open` workaround; recent security audits report `groupPolicy=allowlist`.
12. **vault/project-state.md** is a growing paste of identical daily security-audit paragraphs (Sep–Oct). Not a current-state file anymore.

## Recent failures / lessons
- **Offsite backup:** still the #1 unresolved failure (~3 months). Interactive Keychain "Always Allow" or `GOG_KEYRING_BACKEND=file`.
- **Self-review continuity:** missed 10-09 and 10-11 logs. 10-10 already flagged 10-09. Pattern is "cron ok, artifact sometimes not written" — or the job did not complete.
- **2026-04-17 heartbeat fabrication rule in SOUL.md is still the right hard rule.** HEARTBEAT.md matches it.
- **Do not consolidate MEMORY.md** (SOUL) vs AGENTS "vector memory / 6400 lines" vs MEMORY pending item "nightly consolidation overwrites manual updates" — three-way conflict. Diamond owns MEMORY.md.

## Recommendations (priority unchanged)
1. Fix gog keyring / offsite Drive upload. Everything else is documentation drift.
2. Update SOUL / WORKSPACE / MEMORY model sections to live routing, or pin the model and make docs match.
3. Correct AGENTS.md MEMORY line count; remove nano-banana-pro; pick one web_search rule after one live test.
4. Rename `skills/intake/skill.md` → `SKILL.md`.
5. Reconcile WORKSPACE.md §5–§6 with actual cron locations and `scripts/backup_agents.sh`.
6. Decide: follow decisions-log rule, or stop claiming it in SOUL.
7. Cull/confirm: minimax-image, overlapping browser/X skills, unused report/dashboard/notification/weekly-report skills.
8. Redact the two MEMORY.md tokens.
9. Check why 10-09 and 10-11 self-reviews produced no log.

No core-file edits this run.
