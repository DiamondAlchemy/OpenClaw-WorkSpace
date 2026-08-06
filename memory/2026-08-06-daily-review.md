# Daily Self-Review — 2026-08-06 (Thursday)

## Overview

- **Trigger:** Daily Self-Review cron, 08:00 America/Chicago
- **Files audited:** SOUL.md, WORKSPACE.md, IDENTITY.md, AGENTS.md, MEMORY.md (structure only)
- **Skills inventory:** `skills/` directory — 18 entries
- **Previous review:** 2026-07-28 (9-day gap)
- **No edits made during this audit.**

---

## 1. MEMORY.md Structure

- 153 lines, 12 sections, structurally clean
- Last-updated timestamp `2026-03-22` is stale (~4.5 months old)
- "Promoted From Short-Term Memory (2026-07-17)" footer present — promotion metadata intact
- No malformed markdown, no orphaned headers, no duplicate sections
- Backup files present at root: `MEMORY.md.backup_20260313`, `MEMORY.md.backup_20260313_081736`, `MEMORY.md.backup_20260313_081812`, `MEMORY.md.before-2026-05-07-hermes-role-lane-update` — could be archived/moved out of root for cleanliness

## 2. Core Files

### SOUL.md (modified Apr 17, 2026)
- Hard-rule "NEVER Fabricate Data" section present with 2026-04-17 Scaramanga incident reference — solid
- Change Approval Protocol enumerated (5 categories) — current
- Hermes role-lane guidance embedded (MoneyPenny = alert messenger, not primary orchestrator) — current
- Per-group Telegram authorization (Cannascend, HRBD, Main) — current
- Section ordering OK: identity → how-you-work → approval → no-fabricate → core-truths → vibe → model-capabilities → continuity → group-security → inter-agent → LCM tools

### WORKSPACE.md (modified Apr 7, 2026 — STALE)
- **Issue 1:** Lists primary model as `minimax/MiniMax-M2.7-highspeed` but MEMORY.md says fallback is `google/gemini-2.5-pro` — minor inconsistency
- **Issue 2:** "Active Missions & Priorities" still says GMP Framework is "Standby" — but Hermes role update on 2026-05-07 restructured responsibilities; section header is still useful but could note Hermes lane
- **Issue 3:** "Daily Self-Review" cron listed at "0 8 * * *" — matches reality
- **Issue 4:** Section 7 ("Installed Skills") is essentially a redirect to AGENTS.md, but the actual skills inventory now lives at `TOOLS.md` → could be consolidated

### IDENTITY.md (modified Mar 5, 2026)
- Clean, minimal, on-tone
- No conflicts with SOUL.md
- "Operational Rules" 1-8 are all current

### AGENTS.md (modified May 30, 2026)
- **Issue:** States `MEMORY.md` is "consolidated (6,400+ lines)" — factually wrong, MEMORY.md is 153 lines
- Smart Loading Protocol still valid
- Skills listed match what's actually installed (18 skills)
- Runtime upgrades section is current (SearXNG, tokenjuice, OAuth models)

### USER.md (modified Mar 5, 2026 — STALE)
- No updates since early setup; Christian info, phone, timezone all still correct per SOUL/vault
- Acceptable, but no recent additions (no notes about Vesper, Hermes, etc.)

### TOOLS.md (modified May 13, 2026)
- **Issue 1:** Lists `nano-banana-pro` as image-gen but on-disk skill is `skills/minimax-image/`. TOOLS.md references a non-existent path.
- **Issue 2:** TOOLS.md skills list contains 13 entries — actual install count is 18 (missing `brave-browser-agent`, `browser-auto-plus`, `google-workspace-operator`, `kpi`, `spreadsheet`, `twitterwebapi`, plus the misnamed `nano-banana-pro`)
- **Issue 3:** No `minimax-image` reference in the skills list

## 3. Skills Directory (18 skills)

```
brave-browser-agent/         google-workspace-operator/
browser-auto-plus/           heartbeat/
chart-image/                 intake/
dashboard/                   invoice/
document-pro/                kpi/
fill-docx-template/          minimax-image/    ← only MiniMax-branded skill
notification-system/         pdf-form-filler/
report/                      spreadsheet/
twitterwebapi/               weekly-report-generator/
```

All directories have a `SKILL.md`. No orphan/stale skills detected.

### Possibly unused
- `minimax-image/` — TOOLS.md says active image-gen is `nano-banana-pro` (which doesn't exist as a skill); `minimax-image/` may be the actual active one. The TOOLS.md doc is wrong, the skill may be correct.
- `intake/` — designed for intake forms; only referenced in skill list, no recent use

## 4. Recent Failures & Lessons

From `vault/project-state.md`:
- **2026-07-27:** Lossless-claw was running 0.9.2 since June 15 — gateway restart was never done. Cron missed restart. **Watch for:** any plugin update that requires a gateway restart.
- **2026-07-10:** Promotion noted 6 inactive agents (Drax, Vesper, Nomí, Scaramanga, Zorin, Moat). MEMORY.md "Agent Ecosystem" table only lists 5 active — silent triage pending.
- **2026-06-30:** `/System/Volumes/Data` hit 100% capacity, blocked scrapes. `workspace-goldfinger` at 257G (`perp_tracker.db-wal` 232G). **Watch for:** silent disk-full failures on cron jobs.
- **2026-06-25 + 2026-06-23 + 2026-06-11:** Daily security audits flagged `apify-lead-generation` suspicious file-read + network-send pattern, missing plugin integrity metadata for `codex`/`tokenjuice`/`voice-call`. **No remediation recorded.**

## 5. Outdated / Conflicting / Undocumented

### Outdated
1. WORKSPACE.md "Active Missions" header references Christian's GMP framework as "Standby" — needs Hermes framing
2. AGENTS.md "6,400+ lines" claim (off by ~42x)
3. TOOLS.md `nano-banana-pro` reference vs on-disk `minimax-image/` skill
4. USER.md has not been touched in 5 months
5. MEMORY.md "Last updated 2026-03-22" stamp — old but explicitly preserved manually

### Conflicts
1. **Model identity:** Current runtime is `minimax/MiniMax-M3` (per session_status), MEMORY.md says `minimax/MiniMax-M2.7-highspeed`, WORKSPACE.md same. **No file says M3.**
2. **Agent ecosystem count:** WORKSPACE.md/MEMORY.md lists 5 active agents; 2026-07-10 promotion noted 6 more configured-but-inactive.
3. **Skills list source of truth:** AGENTS.md says canonical reference is itself; WORKSPACE.md redirects to AGENTS.md; TOOLS.md has the most complete list. **Three competing sources.**

### Undocumented workflows
1. **Daily log gap protocol:** No documented rule for handling multi-day gaps (currently 9 days since last review, 18+ days since 2026-07-10). 
2. **Hermes → MoneyPenny → Diamond alert path:** Mentioned in 2026-05-07 update, but no operational procedure documented.
3. **KPI-app MCP reporting path:** Documented in MEMORY.md (2026-05-30), but no examples or escalation pattern when MCP returns nothing.

## 6. Recommendations (NO changes made — Diamond decision)

| Priority | Recommendation |
|----------|----------------|
| HIGH | Reconcile model identity — update MEMORY.md/WORKSPACE.md to reflect current `MiniMax-M3` runtime, or confirm M2.7 is still expected |
| HIGH | Fix TOOLS.md image-gen reference (`nano-banana-pro` → `minimax-image` if that's the active skill) |
| MED  | Update AGENTS.md "6,400+ lines" → actual line count (153) |
| MED  | Triage 6 inactive agents (Drax, Vesper, Nomí, Scaramanga, Zorin, Moat) — confirm if real or remove from config |
| MED  | Decide on canonical skills list (AGENTS.md vs TOOLS.md vs WORKSPACE.md) |
| LOW  | Move stale MEMORY.md backups out of workspace root |
| LOW  | Update USER.md with current operator context (Hermes, Vesper, KPI-app MCP) |
| LOW  | Re-review WORKSPACE.md "Active Missions" — add Hermes lane context |

## 7. Vault Status

- `vault/project-state.md` last updated 2026-07-28 (in this review, will append)
- `vault/decisions-log.md` current through 2026-06-24 entries
- HRBD Telegram group has vault context in decisions-log (2026-04-30 series + 2026-06-02 reports) — not the gap flagged in 2026-07-28 review
