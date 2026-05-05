# Project State — Shared

*Last updated: 2026-05-04*
*Updated by: Vesper*

---

## Active Projects

| Project | Owner | Status | Last Update | Notes |
|---------|-------|--------|-------------|-------|
| Facility Agent System | Q / Diamond | Production | 2026-04-06 | Nomi + Towelie running HRBD + Cannascend |
| cGMP Knowledge Base | Vesper | Ongoing | 2026-04-17 | 79 briefs, regulatory monitoring cron live, first lint pass complete |
| EU-GMP Knowledge Base | Jaws | Complete | 2026-03-25 | 82 briefs, 38-doc library |
| TSW GMP Toolkit | Vesper | In Progress | 2026-05-04 | Christian clarified the standard is the general branded theme used across TSW GMP docs so far, not only the electrical checklist: executive/contractor-facing, black/white/red, clean modern layout, strong cover/header treatment, practical checklist/table structure, version/document metadata, and implementation-focused language. Use that family style consistently for future checklists, SOP templates, BPR templates, QMS docs, and framework deliverables. Electrical checklist remains a good reference: `gmp-electrical-requirements-checklist-branded.html` / `gmp-electrical-requirements-checklist-v1.1-audited.pdf`. New lab building workflow/layout resumed from Christian's hand-marked floor plan image; Vesper confirmed the sketch is readable though a few handwritten labels/dimensions need confirmation. Prior constraint: use only warehouse section and leave bay door space open. Created contractor handoff `gmp-epoxy-flooring-contractor-checklist.md` and branded audit-ready versions `gmp-epoxy-flooring-contractor-checklist-branded.html` / `.pdf` (v1.1 with auditor evidence package) plus shorter contractor handoff PDF `gmp-epoxy-flooring-contractor-handoff-checklist.pdf`. On 2026-05-04 Christian asked whether the branded epoxy flooring checklist can be used in the GMP framework for an audit; Vesper assessed yes — use as contractor specification/handoff, IQ support, auditor evidence package, and operational reference. Christian then confirmed all GMP framework docs must include controlled-document elements by default: document number, version, effective date, approval/signature fields, revision history, page numbering, and clear metadata; this is now the standard for future TSW GMP documents. Created controlled dry-cure sugar records package: `templates/MBR-SUGAR-DC-001_Master_Batch_Record_Dry_Cure_Sugar.md` and `templates/BPR-SUGAR-DC-001_Batch_Production_Record_Dry_Cure_Sugar.md`, both with required GMP document-control elements. Christian then confirmed hydrocarbon sugar operating assumptions; MBR/BPR were revised from dry-cure-only assumptions to cover dry cure trim/flower and fresh frozen whole flower with 9 lb and 15 lb per 6×48 column placeholders, 100% n-butane, 5:1 vs 7:1 solvent ratios, -60°C vs -80°C extraction targets, nitrogen pressure ranges, 65–80°F collection, documented off-gas/LEL measurement, crystallization ramp/break-mix logic, 75–80°F/20 inHg purge cycles, and jar/clamp-seal packaging. Initial audit review found the package is structurally strong but still needs supporting controlled logs/forms before framework-ready use: daily room/equipment readiness log, LEL calibration/bump log, molecular sieve replacement/status log, vacuum oven crystallization/purge log, chiller/freezer temperature log, equipment cleaning/sanitation records tied to the BPR, solvent/nitrogen usage reconciliation, deviation trigger form, and QC release checklist. Prior HRBD Billings layout files remain: raw/gmp-floor-plan-clean.png, raw/blueprint-gmp-zones-v10.png |
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
