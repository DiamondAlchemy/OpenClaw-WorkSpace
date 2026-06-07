# Decisions Log — Shared

*Append-only. Never delete entries. Newest at bottom.*

---

## 2026-03

- **2026-03-20** — Facility agent system deployed. Towelie on Cannascend, M2.5-highspeed. Golden rules established.
- **2026-03-23** — Vesper cGMP engine launched. 67 briefs on first build.
- **2026-03-25** — Jaws EU-GMP engine completed. 82 briefs, 38-doc library.
- **2026-03-27** — Drax CAD system: 14x12 booth layout finalized, 27 equipment renders.
- **2026-03-28** — Silva Google Ads agent: 6 campaigns, stealth strategy for topsecretworkshops.com.
- **2026-03-30** — Towelie retrain after MEMORY.md wipe. Lesson: never aggressively trim training files.

## 2026-04

- **2026-04-01** — OpenRouter setup. Upgraded to OpenClaw 4.1 then 4.2. Broken symlinks fixed with rsync.
- **2026-04-04** — Nomi cloned as Towelie trainer for HRBD. Qwen 3.6 tested and rejected (hallucinates). M2.5 stays for execution.
- **2026-04-06** — Z.ai provider added. GLM-5-Turbo on Nomi, Vesper, Octopussy. QMD installed, dreaming enabled. 00qm00qm killed.
- **2026-04-07** — Scaramanga lead gen agent created. Octopussy on GLM-5.1.
- **2026-04-09** — Shared vault created for knowledge agents. Goldfinger switched to GLM-5.1.
- **2026-04-27** — Reporting COGS rule confirmed by Diamond: every client report must include all operating costs with available data. Biomass-only cost-per-gram is not acceptable unless explicitly labeled. Include available biomass/materials, solvents, gases, nitrogen, CO2, CRC/media, labor, packaging, toll/buyback terms, and any other tracked operating expenses; mark missing categories as Not Available/Not Tracked.
- **2026-04-27** — CO2 cost handling confirmed: CO2 is a major operating cost and must always be included in operating COGS when usable CO2 usage/rate data exists. If unavailable, mark CO2 as Not Available rather than omitting it.
- **2026-04-27** — Butane cost handling corrected: residual solvent/transfer loss is required for calculating actual butane cost and must remain in reports. Butane COGS should use recorded residual loss/lost solvent when available, rather than treating residual loss as an optional chart-only metric.

- **2026-04-30** — HRBD March reporting CO2 rate updated to $100/column per Christian. Regenerated report as v10 and enlarged farm/company origin callouts so it is clearer which farm/company ran which numbers.

- **2026-04-30** — HRBD March v11 generated to fix origin-card text overlap: finished output now uses fixed-width stat columns separate from cost/COGS values.

- **2026-04-30** — HRBD March v12 generated: visible origin-card label changed to “columns ran”; CO2 remains calculated internally at $100/column.

- **2026-04-30** — HRBD March v13 generated after independent math audit. Cost model already used 24 columns and $100/column CO2; fixed chart donut that was still hardcoded at 23 columns.

- **2026-05-02** — TSW GMP framework document style standardized: use the existing black/white/red branded checklist theme from `gmp-electrical-requirements-checklist-branded.html` for all future GMP framework deliverables, including checklists, SOP templates, BPR templates, and QMS documents.

- **2026-05-02** — Clarification from Christian: the design standard is the overall TSW GMP document family/theme used across deliverables so far, not just the electrical checklist. Future docs should preserve the executive/contractor-facing black-white-red branded style, clean modern headers/covers, practical tables/checklists, metadata/versioning, and implementation-focused tone.

- **2026-05-04** — Christian confirmed all TSW GMP framework documents must include controlled-document elements by default: document number, version, effective date, approval/signature fields, revision history, page numbering, and clear document metadata. These are required because TSW is building a GMP framework, not standalone informal handouts.

- **2026-05-04** — Sugar hydrocarbon process parameters confirmed by Christian for controlled record drafts: two material options are dry cure trim/flower and fresh frozen whole flower; placeholder column loads are 9 lb dry cure and 15 lb fresh frozen per 6 in × 48 in column; solvent is 100% n-butane; solvent ratios are 5:1 for dry cure and 7:1 for fresh frozen; extraction targets are -60°C dry cure and -80°C fresh frozen with approved operating range -60°C to -80°C; solvent vessel nitrogen pressurization is 35–45 PSI; column evacuation nitrogen is 45–55 PSI with inert gas vent/repressurization sweep; collection temperature is 65–80°F; off-gas is minimum 3 hours but must include documented solvent/LEL measurement before transfer; crystallization starts at 65°F agitated with +5°F ramps every 12–24 hours and break/mix at 75–80°F; purge is 75–80°F at 20 inHg for 8–12 hours minimum per cycle, remove/mix/repeat for second purge; final packaging may use cleaned glass mason/canning jars or clamp-seal vessels sized to yield.


- **2026-05-04** — Butane LEL documentation standard for sugar/hydrocarbon transfer: record butane LEL reference as 1.8% v/v, but do not use 1.8% as the release threshold. Transfer from C1D1/off-gas to C1D2/post-processing requires a calibrated gas detector reading below the approved site action threshold; recommended default is ≤10% LEL unless AHJ/site policy is stricter. Visual cues and elapsed off-gas time are supporting observations only and cannot replace the documented gas detector reading.

- **2026-05-06** — Christian clarified the current MMR/MBR/BPR/framework documents are internal TSW framework/build docs, not final client-facing/auditor-facing controlled documents. Keep internal document structure practical and implementation-focused; use controlled-document elements where useful, but avoid over-polishing or treating internal drafts as issued client records until converted for a specific client/facility.

- **2026-05-08** — Supersedes 2026-05-04 LEL default language: do **not** state a recommended default of ≤10% LEL in framework documents. Current hydrocarbon/sugar standard is: n-butane LEL 1.8% v/v may be listed as a reference value only; transfer/release decisions require calibrated detector readings below the site-approved action threshold established by AHJ/fire code, safety SOP, equipment requirements, and facility policy.

- **2026-05-10** — RCA framework will use Christian’s TSW 5M method as the primary root-cause structure: Man, Material, Machine, Measurement, and Maintenance, with Mother Nature as a rare/optional sixth M for environmental/natural external causes.

- **2026-05-10** — Christian clarified the TSW RCA structure should not be treated as boilerplate fishbone. The 5M method came from a 35-year experienced injectable GMP site lead and should be treated as the preferred practical GMP RCA model for TSW framework documents.

- **2026-05-10** — Christian clarified that Vesper should not rely on the Mac mini workspace as the only save location. For framework deliverables/corrections, send hard-copy packets directly to Christian/Diamond via Telegram when created or materially updated, so they can save local copies. Hard copies/direct delivery are the preferred robust archive path.

- **2026-05-10** — Christian clarified that Vesper should not rely on the Mac mini workspace as the only save location. For framework deliverables/corrections, send hard-copy packets directly to Christian/Diamond via Telegram when created or materially updated, so they can save local copies. Hard copies/direct delivery are the preferred robust archive path.

- **2026-05-10** — Framework archive rule confirmed by Christian: always save deliverables/corrections in Vesper workspace **and** provide hard-copy packets directly to Christian/Diamond for local saving. Both are required; neither replaces the other.

- **2026-05-10** — Framework archive rule confirmed by Christian: always save deliverables/corrections in Vesper workspace **and** provide hard-copy packets directly to Christian/Diamond for local saving. Both are required; neither replaces the other.

- **2026-05-27** — Diamond approved private GitHub repo sync for the Vesper GMP library. Created `DiamondAlchemy/vesper-gmp-library` as a private, clean export repo instead of pushing the full local workspace history. Initial export includes GMP briefs, EU briefs, libraries, active templates, navigation files, log, and maintenance tools; excludes raw sources, vault notes, memory, temp/packet folders, client folders, binaries, local runtime config, and credentials. Christian access is pending his GitHub username/email.

- **2026-05-10** — Framework archive rule confirmed by Christian: always save deliverables/corrections in Vesper workspace **and** provide hard-copy packets directly to Christian/Diamond for local saving. Both are required; neither replaces the other.

- **2026-05-28** — Diamond approved expanding `DiamondAlchemy/vesper-gmp-library` for Hermes framework work. The approved repo scope now includes controlled PDF/reference folders (`briefs-pdf/`, `regulatory-updates-pdf/`, `framework-pdf/`), editable framework source under `framework-source/`, selected safe source references under `sources-approved/`, and `MANIFEST.md`. The exclusion rule remains: no vault/memory/runtime state, client blueprints/images, private raw workspace material, temp files, ZIP packets, credentials, or local config.

- **2026-05-29** — Diamond switched MoneyPenny back to GPT for default operation after briefly testing Sonnet. Operational preference: stay on GPT normally, with Sonnet available to switch to when needed for a specific task.

- **2026-05-30** — KPI-app MCP is the fleet reporting path. Diamond's engineering Claude briefed that agents should use the read-only KPI-app MCP for cost, yield, throughput, manifest, process, and dashboard reporting once bridged. It routes through app auth, facility scoping, and audit logging. The raw read-only Postgres MCP exists but bypasses those app controls and remains Diamond-only; agents should not request or use raw DB/SQL for reporting. The KPI-app bridge is coming via HTTP, named cloudflared tunnel, and API key, like Hermes.

- **2026-05-31** — Diamond approved and requested installation of Tanner scout item #1, the ClawHub `twitterwebapi` skill. Installed `twitterwebapi@1.0.0` in MoneyPenny's workspace for X/Twitter tweet detail and timeline search. Free-tier test worked once, then the free daily credit was exhausted; paid/high-frequency use requires `AZT_API_KEY`. Local wrapper was patched to support returned `timeline` search data and subcommand-position `--json`.

- **2026-06-01** — Claude/Diamond Vesper consolidation decision: the US and EU GMP libraries move to maintain-only. Automated brief producers and EU firehose are off; monitor/lint remain on. New briefs should be demand-driven gap fillers from `research-backlog.md`, not automatic curriculum expansion. `STATE.md` is the single source of truth for counts.

- **2026-06-01** — Framework ownership decision: Christian owns the TSW GMP framework build. Vesper does not build SOPs, MBRs, BPRs, forms, or push to Christian's repo unless explicitly delegated. Vesper keeps `christian-framework-clone/` as a read-only backup/audit source and treats `tsw-unified-framework/` as a one-time reference snapshot. Hydrocarbon remains the active framework focus; CO2 and ethanol are back-burner.

- **2026-06-01** — Audit standard confirmed for Christian framework work: Vesper may perform read-only audits against verified briefs and primary sources, producing intel reports such as `CHRISTIAN-FRAMEWORK-AUDIT.md`, but must not modify Christian's repo or turn audit findings into Vesper's own build queue without delegation.

- **2026-06-07** — Diamond approved installing Tanner scout 2026-06-06 items #1-#5. Installed `google-workspace-operator`, `browser-auto-plus`, `brave-browser-agent`, `googlechat`, and `google-meet`. Google Chat and Google Meet require a gateway restart to load. Google Workspace is installed but requires the TangleClaw Google OAuth plugin/config dependency before its tools are usable.
