# Daily Self-Review — 2026-07-28 (Tuesday)

**Reviewer:** MoneyPenny (cron-triggered, agent:main)
**Scope:** SOUL.md, AGENTS.md, IDENTITY.md, USER.md, WORKSPACE.md, MEMORY.md (structural only), TOOLS.md, skills/, vault/

---

## 1. Core file freshness

| File | Last modified | Status |
|---|---|---|
| SOUL.md | 2026-04-17 | Stable. No drift. |
| IDENTITY.md | 2026-03-05 | Stable. |
| USER.md | 2026-03-05 | Stable. Note: "Alvie has been working to get this environment running for several days" is now 4+ months stale (cosmetic). |
| AGENTS.md | 2026-05-30 | Stable. |
| WORKSPACE.md | 2026-04-07 | Stable reference doc. |
| TOOLS.md | 2026-05-13 | **Stale skills list** (see §4). |
| MEMORY.md | 2026-07-17 | Promoted-content update; header "Last updated: 2026-03-22" is by-design stale (Diamond maintains manually). |
| DREAMS.md | 2026-07-28 03:05 | Active dreaming pipeline — last night rem/deep/light all fired. |

No file has drifted into dangerous territory. SOUL.md change-approval protocol and NEVER-fabricate rule are intact and consistent.

## 2. MEMORY.md structure (no content read)

153 lines, 13 H2 sections, ~11.4 KB. Sections (in order):

1. System & Configuration
2. People & Contacts
3. Agent Ecosystem (as of 2026-03-22)
4. Facility Agent System (LIVE — 2026-03-20)
5. Workspace Cleanup (2026-03-19/20)
6. Operational Protocols
7. Bugs & Fixes (with lessons)
8. Claude MCP Bridge (2026-05-13)
9. KPI-App MCP Reporting Path (2026-05-30)
10. Pending / Open Items
11. Hermes Role/Lane Update — 2026-05-07
12. Promoted From Short-Term Memory (2026-07-17)

**Observations:**
- The "Agent Ecosystem (as of 2026-03-22)" and "Facility Agent System (LIVE — 2026-03-20)" headings carry March as-of dates. Per the 2026-07-10 promotion in MEMORY.md itself, **Drax/Vesper/Nomí/Scaramanga/Zorin/Moat are configured but inactive** — this contradicts the "LIVE" framing. Flagged for Diamond; per SOUL.md I do not edit MEMORY.md myself.
- The "Promoted From Short-Term Memory (2026-07-17)" section is the only promotion block from the last dreaming cycle. Marker count = 1. Either promotion gating is now very strict, or the dreaming/promotion pipeline has been quiet on substantive content.
- No structural anomalies (broken headers, mismatched backticks, fenced-code-block drift). File is well-formed.

## 3. Daily-log gap (carried over from 2026-07-26 review)

`memory/2026-07-XX.md` is still absent for 2026-07-11 → 2026-07-26. Last human-style log: `2026-07-10.md`. The 16-day gap persists. This review is once again the only post-2026-07-10 file write.

**Implication:** AGENTS.md "Immediate Context: today + yesterday" load step has been operating on missing logs for 18 consecutive days. The dreaming pipeline (memory/dreaming/*/2026-07-28.md present) is filling part of the gap with auto-generated reflections, but those are not the same as session daily logs.

## 4. skills/ directory (18 entries, all healthy)

```
brave-browser-agent         OK (252 lines)  2026-06-07
browser-auto-plus           OK (225 lines)  2026-06-07
chart-image                 OK (392 lines)  2026-05-13
dashboard                   OK ( 98 lines)  2026-05-13
document-pro                OK (120 lines)  2026-05-13
fill-docx-template          OK (511 lines)  2026-05-13
google-workspace-operator   OK (156 lines)  2026-06-07
heartbeat                   OK (118 lines)  2026-05-13
intake                      OK (291 lines)  2026-05-13
invoice                     OK ( 74 lines)  2026-05-13
kpi                         OK (108 lines)  2026-05-13
minimax-image               OK ( 54 lines)  2026-03-22  ← oldest
notification-system        OK (170 lines)  2026-05-13
pdf-form-filler             OK (164 lines)  2026-05-13
report                      OK (119 lines)  2026-05-13
spreadsheet                 OK (101 lines)  2026-05-13
twitterwebapi               OK ( 99 lines)  2026-05-31
weekly-report-generator     OK ( 58 lines)  2026-05-13
```

All 18 skills have valid SKILL.md. No skill is broken or missing.

**`minimax-image`** (2026-03-22) is the oldest skill — predates the May 13 bulk install by ~2 months. It's the original `minimax-banana-pro`-era skill and was renamed at some point. Worth confirming whether it's still the active image-gen path or whether `nano-banana-pro` referenced in TOOLS.md is a different/separate thing. **TOOLS.md says `nano-banana-pro` is the active image-gen path** (under Image Generation section) — that suggests `minimax-image` may be **unused/legacy** while a different `nano-banana-pro` skill (not present in `skills/`) handles image generation. Conflict.

**TOOLS.md skill list is stale:** the file lists 13 skills; the directory has 18. Missing from TOOLS.md: `brave-browser-agent`, `browser-auto-plus`, `google-workspace-operator`, `twitterwebapi`, `minimax-image`. TOOLS.md also lists `nano-banana-pro` which doesn't exist in `skills/`.

## 5. Conflicts / outdated info / undocumented workflows

**Conflicts:**

- **TOOLS.md vs skills/ reality:** TOOLS.md says `nano-banana-pro` is the active image-gen provider, but no `nano-banana-pro/` skill directory exists. `skills/minimax-image/` is present and dated 2026-03-22. Either TOOLS.md is referring to an external skill, the skill was renamed and the directory needs renaming, or `minimax-image` is dead and TOOLS.md should be updated to reflect what's actually installed.
- **SOUL.md group authorization:** the `HRBD` group (`-1003872220174`) has no corresponding context anywhere — no `hrbd/` directory, no entry in vault, no reference in decisions-log. Either it's a vestigial group or a recent auth list drift.
- **MEMORY.md "LIVE 2026-03-20" framing vs 2026-07-10 promotion note** (Drax/Vesper/Nomí/Scaramanga/Zorin/Moat unused). Contradiction noted, not edited.
- **`memory_curator.py` vs SOUL.md rule.** SOUL.md says "Diamond maintains MEMORY.md manually — do not overwrite, regenerate, or consolidate." But `memory_curator.py` (workspace root, 2026-03-04) and `ai_consolidate_memory.py` (workspace root, 2026-03-18) both exist. MEMORY.md itself references "ai_consolidate_memory.py" as the consolidation script. This is a real conflict between SOUL.md (which I treat as authoritative) and the tooling that exists on disk. **The 2026-07-10 promotion block was apparently added by the dreaming pipeline without my intervention**, suggesting the dreaming/promotion path does touch MEMORY.md — likely outside my scope but in tension with the "manual only" rule. Flagged.

**Outdated info:**

- USER.md "Alvie has been working to get this environment running for several days" → months old. Cosmetic.
- AGENTS.md "MEMORY.md consolidation complete (6,400+ lines)" → MEMORY.md is 153 lines, not 6,400. This line is factually wrong now and should be deleted or rephrased. Same finding as 2026-07-26 review — not yet fixed.
- TOOLS.md skills list (see above).
- MEMORY.md header "Last updated: 2026-03-22" — by-design stale, but worth knowing.

**Undocumented workflows:**

- `protocols/telegram-scrape.md` and `protocols/telegram-scrape-gemini.md` (both 2026-03-09) — referenced by no document. Still on disk.
- `workspace-shared/.mcp.json` (2026-04-26) — MCP config exists but is not documented in AGENTS.md or SOUL.md.
- `/Users/m/.openclaw/tools/` contains several scripts (`agent_message.py`, `gateway-nightly-restart.sh`, `openclaw-mcp-daemon.sh`, `ralph`, etc.) — only `agent_message.py` is documented in TOOLS.md. Others are likely Hermes/Tanner/Q tooling, but undocumented.
- `moneypenny/` subdirectory is a separate workspace clone (its own AGENTS.md, SOUL.md, MEMORY.md) — appears to be the MoneyPenny-pinned workspace, but neither AGENTS.md nor SOUL.md mentions that this exists or that there are now two parallel workspaces.

**Recent failure lessons:**

- 2026-04-17 fabrication incident (heartbeat enrichment inventing cannabis business contacts) — captured in SOUL.md "NEVER Fabricate Data" rule and reinforced in HEARTBEAT.md. Strong rule.
- 2026-06-30 disk-full incident (Goldfinger WAL at 232G → Telegram scrapes failing) — captured in project-state.md, root-caused and reported.
- 2026-06-25 / 2026-06-11 security audit findings — captured in project-state.md (warnings about Telegram groupPolicy="open", plugin integrity, apify-lead-generation code pattern). Open risk: the `groupPolicy="open"` Telegram finding from 2026-06-11 was flagged as 14 critical. Status as of today: not clear whether closed.

## 6. Recommendations (no changes made — reporting only)

1. **Diamond decision:** `minimax-image` skill vs `nano-banana-pro` reference in TOOLS.md — confirm which is active and whether `skills/minimax-image/` should be renamed, deleted, or left alone.
2. **Diamond decision:** Is MEMORY.md's "Agent Ecosystem (as of 2026-03-22)" still authoritative, given the 2026-07-10 promotion note flagging 6 agents as inactive?
3. **Daily-log gap** is now 18 days. Suggest Diamond decide: backfill 2026-07-11 → 2026-07-27, or accept the gap. The dreaming pipeline is covering some ground but is not equivalent to daily session logs.
4. **AGENTS.md "6,400+ lines"** line is factually wrong — single-line edit when convenient.
5. **TOOLS.md skills list** is missing 5 installed skills. Refresh when convenient.
6. **HRBD Telegram group** in SOUL.md auth list has no vault/workspace context — confirm still live or remove.
7. **`memory_curator.py` + `ai_consolidate_memory.py`** conflict with SOUL.md's "Diamond maintains MEMORY manually" rule. The dreaming pipeline appears to add promoted sections to MEMORY.md via `ai_consolidate_memory.py`. Clarify intent: either SOUL.md should explicitly authorize the dreaming/promotion path, or the dreaming pipeline should not write to MEMORY.md.
8. **`moneypenny/` parallel workspace** — worth a one-line purpose note in AGENTS.md or SOUL.md so future-me knows why two MoneyPenny workspaces exist.
9. **`protocols/telegram-scrape*`** files have no AGENTS.md pointer — link or remove.
10. **`workspace-shared/.mcp.json`** — undocumented MCP config. Either link from AGENTS.md or remove.
11. **Security audit follow-up:** 2026-06-11 audit reported 14 critical findings (Telegram `groupPolicy="open"` plus google-meet child_process pattern). Status unknown; worth a re-audit or explicit close-out.

---

*Self-review complete. No files modified. Findings above are observational only and subject to Diamond's judgment.*