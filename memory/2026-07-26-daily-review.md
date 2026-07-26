# Daily Self-Review — 2026-07-26 (Sunday)

**Reviewer:** MoneyPenny (cron-triggered, agent:main)
**Scope:** SOUL.md, AGENTS.md, IDENTITY.md, USER.md, MEMORY.md (structural), TOOLS.md, skills/

---

## 1. Core file age & freshness

| File | Last modified | Note |
|---|---|---|
| SOUL.md | 2026-04-17 | Stable, personification file. OK. |
| IDENTITY.md | 2026-03-05 | Stable. OK. |
| USER.md | 2026-03-05 | Stable. OK. |
| AGENTS.md | 2026-05-30 | Stable. OK. |
| TOOLS.md | 2026-05-13 | Lists `web_search.py` script + manual web_search bypass. Skills list inside it is stale — see below. |
| MEMORY.md | 2026-07-17 (promoted section header) | Header says "Last updated: 2026-03-22 (manual update — do not overwrite)". Body is now dated 2026-07-17 via promotion block. |

**MEMORY.md internal date mismatch** — header reads "Last updated: 2026-03-22" but the last `## Promoted From Short-Term Memory (2026-07-17)` section is from July. The header is stale by design (Diamond maintains manually per SOUL.md) but the *promotion* block now spans a 4-month gap. No action — flagged only.

## 2. MEMORY.md structure

153 lines. 13 H2 sections. 1 promotion comment block (single tagged line — promotes itself rather than multiple). Sections present:

- System & Configuration
- People & Contacts
- Agent Ecosystem (as of 2026-03-22)
- Facility Agent System (LIVE — 2026-03-20)
- Workspace Cleanup (2026-03-19/20)
- Operational Protocols
- Bugs & Fixes (with lessons)
- Claude MCP Bridge (2026-05-13)
- KPI-App MCP Reporting Path (2026-05-30)
- Pending / Open Items
- Hermes Role/Lane Update — 2026-05-07
- Promoted From Short-Term Memory (2026-07-17)

**Anomalies / observations:**
- The "Agent Ecosystem (as of 2026-03-22)" and "Facility Agent System (LIVE — 2026-03-20)" headings carry dates from March. These were accurate as-of dates, but the 2026-07-10 promotion note in MEMORY itself says: "Several agents (Drax, Vesper, Nomí, Scaramanga, Zorin, Moat) are configured but I haven't gotten any signal they're active or being used. Worth a separate triage if Diamond wants to know." This is a fresh observation that contradicts the "LIVE" framing from March.
- "Promoted From Short-Term Memory (2026-07-17)" has only **one** promoted item in it (the secondary-observations note about heartbeat silence). The promotion marker count = 1. Either promotion gating is now very strict, or the dreaming/promotion pipeline has been quiet.
- Per SOUL.md hard rule: **do not consolidate MEMORY.md myself.** All findings flagged, not fixed.

## 3. memory/ daily logs gap

**Critical finding:** No `memory/2026-07-XX.md` file exists for any day from 2026-07-11 through 2026-07-26 (today). The most recent daily log is `2026-07-10.md`. That's a **16-day gap**.

Implications:
- The "Immediate Context: today + yesterday" load step (AGENTS.md protocol) has been operating on stale or missing logs every session for 2+ weeks.
- This review is the first post-gap memory write — and it's the review itself, not a normal session log.
- Heartbeat-state.json still references email/drive polling at unix 1783498016 = mid-July; live status unknown.

## 4. skills/ directory (18 entries)

```
brave-browser-agent
browser-auto-plus
chart-image
dashboard
document-pro
fill-docx-template
google-workspace-operator
heartbeat
intake
invoice
kpi
minimax-image
notification-system
pdf-form-filler
report
spreadsheet
twitterwebapi
weekly-report-generator
```

**Observations:**
- All skills installed 2026-05-13 (bulk install) except `brave-browser-agent`, `browser-auto-plus`, `google-workspace-operator` (Jun 7) and `twitterwebapi` (May 31), plus `minimax-image` which is dated **2026-03-22** — much older than the rest. That predates the May 13 bulk install by ~2 months. It's the original "minimax-banana-pro"-era skill. May be inactive.
- TOOLS.md (May 13) advertised: chart-image, report, dashboard, notification-system, heartbeat, kpi, spreadsheet, fill-docx-template, pdf-form-filler, document-pro, intake, invoice, weekly-report-generator. **Missing from TOOLS.md:** `brave-browser-agent`, `browser-auto-plus`, `google-workspace-operator` (newer), `twitterwebapi` (newer), `minimax-image` (old). → **TOOLS.md skill list is stale.** It's missing 5 installed skills, and the install dates inside skills/ confirm those skills are present on disk.

## 5. Conflicts / outdated info / undocumented workflows

**Conflict — authorized Telegram groups in SOUL.md:**
SOUL.md hard-codes three Telegram group IDs (Cannascend, HRBD, Main). The HRBD group (`-1003872220174`) is named "HRBD" — there's no `hrbd/` directory or context in `vault/`. Either HRBD was renamed, deprecated, or the auth list drifted. Worth asking Diamond.

**Undocumented workflows observed in code/files but not in SOUL.md/AGENTS.md:**
- `telegram-scrape-gemini.md` and `telegram-scrape.md` exist in `protocols/` (dated March 9). Not referenced from AGENTS.md or SOUL.md.
- `memory_curator.py` lives at workspace root — a script that mutates MEMORY.md? Not documented anywhere I can see; SOUL.md says Diamond maintains MEMORY manually. Potential conflict.
- `agent_message.py` at `/Users/m/.openclaw/tools/` is documented in TOOLS.md, good.

**Stale/outdated info:**
- AGENTS.md says "MEMORY.md consolidation complete (6,400+ lines)" — actual file is **153 lines**. The consolidation referenced is the *old* one. The phrase should be updated or removed, since MEMORY.md is now a small curated file, not a 6,400-line corpus.
- USER.md line "Alvie has been working to get this environment running for several days" — from March. That's been true for **months**, not days. Cosmetic but worth refreshing if anything else in that file changes.
- `moneypenny/` subdirectory at workspace root has items dated 2026-07-26 (today) — that's likely an active working area, but I have no documentation of what lives there vs. the workspace root. Worth a one-line purpose note.

**Recent failure lessons already captured well:**
- 2026-04-17 fabrication incident (heartbeat enrichment inventing phone numbers) — SOUL.md documents this explicitly with the "NEVER Fabricate Data" rule. Good.
- MEMORY.md "Bugs & Fixes (with lessons)" section exists for this purpose.

## 6. Recommendations (no changes made)

1. **Diamond decision needed:** Is MEMORY.md's "Agent Ecosystem (as of 2026-03-22)" still the source of truth? If Drax/Vesper/Nomí/Scaramanga/Zorin/Moat are unused, the "LIVE" framing should be retired.
2. **Daily logs gap** — backfill or skip? The 16-day absence since 2026-07-10 is significant. Suggest Diamond decide whether to backfill 2026-07-11…25 or accept the gap.
3. **TOOLS.md skill list** is missing 5 currently-installed skills. Worth refreshing in a future manual edit (Diamond maintains this file area).
4. **AGENTS.md "6,400+ lines" line** is factually wrong now. Cosmetic; suggest one-line edit when convenient.
5. **HRBD Telegram group** in SOUL.md auth list has no corresponding context anywhere in the vault or workspace — confirm it's still live.
6. **`protocols/telegram-scrape*`** files exist with no AGENTS.md pointer. Either link them from AGENTS.md or remove if stale.
7. **`memory_curator.py`** at workspace root may conflict with the "Diamond maintains MEMORY manually" rule. Confirm intent.
