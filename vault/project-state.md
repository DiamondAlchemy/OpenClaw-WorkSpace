# Project State — Shared

*Last updated: 2026-05-02*
*Updated by: Vesper*

---

## Active Projects

| Project | Owner | Status | Last Update | Notes |
|---------|-------|--------|-------------|-------|
| Facility Agent System | Q / Diamond | Production | 2026-04-06 | Nomi + Towelie running HRBD + Cannascend |
| cGMP Knowledge Base | Vesper | Ongoing | 2026-04-17 | 79 briefs, regulatory monitoring cron live, first lint pass complete |
| EU-GMP Knowledge Base | Jaws | Complete | 2026-03-25 | 82 briefs, 38-doc library |
| TSW GMP Toolkit | Vesper | In Progress | 2026-05-01 | New lab building workflow/layout paused MMR. Christian uploaded blueprint `raw/blueprint-entryway/source.pdf`; converted image at `raw/blueprint-entryway/page-1-small.png`. Constraint: use only warehouse section and leave bay door space open. Initial read: warehouse approx 60' wide; bay/logistics area lower-left should remain open; proposed flow receiving → quarantine → released raw storage → production/post-process → packaging → finished goods → shipping. Created contractor handoff `gmp-epoxy-flooring-contractor-checklist.md` for cGMP-style resinous flooring requirements. Awaiting room list/sizes. Prior HRBD Billings layout files remain: raw/gmp-floor-plan-clean.png, raw/blueprint-gmp-zones-v10.png |
| Drax CAD System | Drax | Testing | 2026-04-03 | 63K lines, 48/48 tests, Diamond testing via TG |
| Google Ads / Silva | Silva | Paused | 2026-03-28 | 6 campaigns, 170+ keywords, topsecretworkshops.com |
| Scaramanga Lead Gen | Scaramanga | New | 2026-04-07 | Cannabis lead gen, SQLite DB, MT focus |
| Monthly Reports | Octopussy | Ongoing | 2026-04-30 | Audited HRBD March math and regenerated v13. CO2 remains $100/column, visible label remains columns ran, and hardcoded donut-chart CO2 column count was corrected from 23 to actual TOTAL_COLS=24. File: reports/hrbd/monthly/HRBD-March-2026-v13.pdf. |
| Goldfinger Trading | Cryptobot | Active | — | Perp tracking, shadow monitor, shell monitor |

---

## Recent Decisions

| Date | Decision | Context |
|------|----------|---------|
| 2026-04-06 | GLM-5-Turbo for facility agents | Z.ai coding plan, Nomi + Vesper switched |
| 2026-04-06 | QMD + Dreaming enabled | Memory-core plugin, all agents indexed |
| 2026-04-06 | 00qm00qm account dead | Disabled by Google, removed from all scripts |
| 2026-04-06 | Rule 48 added | Read script every message, both Nomi + Towelie |
| 2026-05-01 | New lab layout constraint | Christian requested cGMP workflow for uploaded blueprint: only use warehouse section and leave bay door space open. |

---

## Infrastructure Notes

- **Vision:** Gemini 2.5 Flash (global imageModel), Nemotron workaround ready but untested
- **Z.ai:** Coding plan, glm-5-turbo + glm-5.1 available. No vision (GLM-5V-Turbo not on plan)
- **Memory:** QMD indexed, dreaming at 3 AM, recall stores building
- **gog:** Dead account removed, moneypenny@topsecretworkshops.com is primary
