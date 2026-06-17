# Daily Self-Review — 2026-06-17

[FACT] Self-review cron (71fd569d) ran at 8:00 AM CT.
[FACT] MEMORY.md is 153 lines (not 6,400+ as AGENTS.md claims).
[FACT] Current runtime model is `minimax/MiniMax-M3` per session status.
[FACT] SOUL.md and WORKSPACE.md still document primary as `MiniMax-M2.7-highspeed` — STALE.
[FACT] AGENTS.md still claims "MEMORY.md consolidation complete (6,400+ lines)" — STALE.
[FACT] TOOLS.md documents only 10 of 20 installed skills.
[FACT] TOOLS.md says "do NOT use built-in web_search tool" — but web_search is now a working runtime tool. STALE.
[FACT] Hermes lane update (2026-05-07) is in MEMORY.md but never propagated to SOUL.md, AGENTS.md, or WORKSPACE.md. MoneyPenny's public role descriptions still call her "orchestrator" / "MI6 digital handler".
[FACT] Stale MEMORY.md backups in workspace root: `MEMORY.md.backup_20260313*` (3 files) and `MEMORY.md.before-2026-05-07-hermes-role-lane-update`.
[FACT] `minimax-image` skill last modified 2026-03-22, no documentation in TOOLS.md or AGENTS.md, likely superseded by runtime `image_generate` tool.
[FACT] `twitterwebapi` skill overlaps with runtime-available `xurl` skill. Possible duplication.
[FACT] Vault protocol (read `vault/project-state.md` and `decisions-log.md` on session start, update after every task) lives only in SOUL.md "Shared Vault — MANDATORY" section. Not in AGENTS.md Smart Loading Protocol.
[FACT] Workspace root contains 3 MEMORY.md backups from March 13 (286KB each) and 1 from May 7. All stale.
[FACT] `agent_message.py` documented twice (SOUL.md + WORKSPACE.md §4d) with overlapping content.
[FACT] SOUL.md "Model Capabilities" section still says "MiniMax-M2.7-Highspeed (primary)" — drift.
[FACT] INTER-AGENT MESSAGING — both SOUL.md and WORKSPACE.md document the same `agent_message.py` script.

[LESSON] Daily self-review is catching real drift. Worth keeping as a real cron, not just ceremony.

[RECOMMENDATION] Major SOUL.md/WORKSPACE.md update needed for: (1) Hermes lane, (2) current model M3, (3) tool availability changes (web_search, image_generate, xurl, kpi-app__*), (4) vault protocol integration with Smart Loading.
[RECOMMENDATION] Clean up 4 stale MEMORY.md backups in workspace root.
[RECOMMENDATION] Reconcile `ai_consolidate_memory.py` vs `memory_curator.py` vs "never consolidate MEMORY.md" — pick one and update all three files.
[RECOMMENDATION] Add 9 missing skills to TOOLS.md (or remove unused ones: minimax-image, twitterwebapi).
[RECOMMENDATION] Update AGENTS.md "6,400+ lines" claim to reflect actual 153-line state.
[RECOMMENDATION] Dedupe `agent_message.py` doc — pick SOUL.md or WORKSPACE.md, not both.
