# Project State — Shared

*Last updated: 2026-04-26*
*Updated by: Octopussy*

---

## Active Projects

| Project | Owner | Status | Last Update | Notes |
|---------|-------|--------|-------------|-------|
| Facility Agent System | Q / Diamond | Production | 2026-04-06 | Nomi + Towelie running HRBD + Cannascend |
| cGMP Knowledge Base | Vesper | Ongoing | 2026-04-17 | 79 briefs, regulatory monitoring cron live, first lint pass complete |
| EU-GMP Knowledge Base | Jaws | Complete | 2026-03-25 | 82 briefs, 38-doc library |
| TSW GMP Toolkit | Vesper | In Progress | 2026-04-20 | GMP zone layout for HRBD Billings. v10: horizontal layout with zones spread across full 60' width of warehouse. Zones in horizontal rows: Biomass/Sock (bottom), C1D1/Offgassing/C1D2 (middle), QC/Finished Goods/Office (top). Workflow south-to-north. Files: raw/gmp-floor-plan-clean.png, raw/blueprint-gmp-zones-v10.png |
| Drax CAD System | Drax | Testing | 2026-04-03 | 63K lines, 48/48 tests, Diamond testing via TG |
| Google Ads / Silva | Silva | Paused | 2026-03-28 | 6 campaigns, 170+ keywords, topsecretworkshops.com |
| Scaramanga Lead Gen | Scaramanga | New | 2026-04-07 | Cannabis lead gen, SQLite DB, MT focus |
| Monthly Reports | Octopussy | Ongoing | 2026-04-27 | Updated HRBD March v8 report so COGS by originating entity is split by material type (FF vs Dry Cure), not blended. CO2 must always be included as a major COGS component when usable CO2 data/rate exists. Residual solvent/loss is required because it drives actual butane cost, so residual loss stays in the report. Next report iteration should restore a pie/donut chart and add lab-ops/light-finance charts in the current theme. File: reports/hrbd/monthly/HRBD-March-2026-Operating-Costs-v8.pdf. |
| Goldfinger Trading | Cryptobot | Active | — | Perp tracking, shadow monitor, shell monitor |

---

## Recent Decisions

| Date | Decision | Context |
|------|----------|---------|
| 2026-04-06 | GLM-5-Turbo for facility agents | Z.ai coding plan, Nomi + Vesper switched |
| 2026-04-06 | QMD + Dreaming enabled | Memory-core plugin, all agents indexed |
| 2026-04-06 | 00qm00qm account dead | Disabled by Google, removed from all scripts |
| 2026-04-06 | Rule 48 added | Read script every message, both Nomi + Towelie |

---

## Infrastructure Notes

- **Vision:** Gemini 2.5 Flash (global imageModel), Nemotron workaround ready but untested
- **Z.ai:** Coding plan, glm-5-turbo + glm-5.1 available. No vision (GLM-5V-Turbo not on plan)
- **Memory:** QMD indexed, dreaming at 3 AM, recall stores building
- **gog:** Dead account removed, moneypenny@topsecretworkshops.com is primary
