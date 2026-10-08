# Daily Self-Review — 2026-10-08

Ran 08:00 CDT via gateway cron. Read-only review of SOUL.md, WORKSPACE.md, IDENTITY.md, AGENTS.md, TOOLS.md, HEARTBEAT.md, MEMORY.md structure, skills/ inventory. No core files changed.

## Repeat findings (unchanged, multi-day)

1. **Model-identity drift.** SOUL.md/WORKSPACE.md/AGENTS.md document MiniMax-M2.7-Highspeed as primary (Gemini fallback, "cannot see images"). Live session: `zai/glm-5.3-flash`, fallbacks zai + `google/gemini-flash-latest`; runtime default_model=xai/grok-4.6. AGENTS.md model-capabilities routing guidance is stale.
2. **AGENTS.md MEMORY.md size claim wrong.** Says 6,400+ lines; actual 153 lines / 11,135 bytes.
3. **TOOLS.md points at non-existent skill.** nano-banana-pro is not in workspace/skills/ nor bundled openclaw skills (only nano-pdf). Command would fail.
4. **TOOLS.md vs AGENTS.md contradiction on web search.** TOOLS.md: "Do NOT use built-in web_search — broken upstream." AGENTS.md: "Use web search normally; defaults to local SearXNG." One is wrong; needs verification.
5. **skills/intake/ has `skill.md` (lowercase)**, not SKILL.md — loader may ignore it.
6. **WORKSPACE.md §5 cron table doesn't match reality.** Gateway cron (main agent) shows exactly 1 job: Daily Self-Review. Security audit + GitHub sync demonstrably ran 10-06/10-07 (logs/git), so they're scheduled somewhere not reflected in docs; full-system backup_to_drive.sh cadence (4am/4pm) unverifiable. System crontab carries additional unexplained jobs (scrapes, moat refresh, watchdog, nightly restart/repo backup).
7. **TOP unresolved: offsite backup auth broken ~2 months.** Drive upload of daily agent backups failing on gog keyring timeout (moneypenny@topsecretworkshops.com) since at least 07-12/09-01. Local archives pass `zip -T` daily. Likely tied to pending MEMORY.md item: gog OAuth re-auth / test-user on consent screen. Still the highest-priority fix.

## New / positive deltas

- **MEMORY.md plaintext tokens: 0 matches** on secret-pattern scan (sk-/ghp_/xox/AIza). Prior reviews flagged two — cleaned since. ✓
- **Promotion footer unstuck.** "Promoted From Short-Term Memory (2026-10-06)" now reflects a recent date (was recycling 2026-07-26). ✓
- GitHub sync healthy: last commit `d98cd2e` 10-07 15:00, daily cadence intact.
- vault/project-state.md current through 10-07. vault/decisions-log.md last touched 06-24 — 3.5 months stale despite SOUL.md rule to append after significant decisions.

## MEMORY.md structure

153 lines, 15 top-level/secondary headings, clean hierarchy, 0 tabs, no CRLF. One long line (108, 579 chars: groupPolicy="open" accepted-risk note) — readable, no action. Last modified 10-06.

## Skills inventory (19 in workspace/skills/)

- minimax-image: stale (Mar 2026, tied to retired MiniMax-primary era) — removal candidate.
- Overlap candidates: brave-browser-agent vs browser-auto-plus; twitterwebapi vs bundled xurl.
- No recent-use evidence for: report, dashboard, notification-system, weekly-report-generator, heartbeat (one-time design use). Harmless but candidates for a cull review.

## Security posture (from 10-07 audit log, no re-run needed)

0 critical / 5 warnings / 2 info, unchanged ~3 weeks: autoAllowSkills, weak_tier on Moat, trust-model heuristic, googlechat plugin tools, apify-lead-generation suspicious pattern (Scaramanga workspace — out of my lane, flagged daily).

## Recommendations (priority order)

1. Fix gog OAuth/keyring for offsite backups (2 months local-only).
2. Update model docs (SOUL/WORKSPACE/AGENTS) to live reality or strip model-specific claims.
3. Remove nano-banana-pro from TOOLS.md; resolve TOOLS-vs-AGENTS web_search contradiction by testing built-in web_search once.
4. Fix AGENTS.md "6,400+ lines" claim; verify smart-loading claim.
5. Rename skills/intake/skill.md → SKILL.md.
6. Reconcile WORKSPACE.md cron table; document where security-audit and backup schedules actually live.
7. Either use decisions-log.md or retire the rule.
8. Cull review: minimax-image, browser-skill overlap, X-skill overlap.
