# Metrc Integration Specification

## Overview
Bidirectional sync between Metrc (cannabis tracking) and Google Sheets (KPI tracker & documentation).

## Workflow: The Complete Loop

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   PULL FROM     │     │   EXTRACTION    │     │   PUSH BACK     │
│   METRC         │────▶│   (Document in  │────▶│   TO METRC      │
│   → Sheets      │     │   Sheets)       │     │   → Complete    │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

## Step 1: Pull from Metrc → Sheets
**Trigger:** New batch identified in KPI tracker

**Data to pull from Metrc:**
- Harvest batch details (strain, weight, date)
- Plant IDs / batch IDs
- Current package status
- Previous extraction data (if any)

**Destination:** Google Sheet (KPI Tracker)

## Step 2: Extraction Process (Sheets)
**Document in Sheets:**
- Start time / end time
- Temperatures
- Solvent used
- Yields
- Notes / observations
- Input weight → Output weight calculations

## Step 3: Push to Metrc → Complete the Loop
**Trigger:** Extraction complete, final metrics entered in Sheets

**Data to push to Metrc:**
- Create package(s) from harvest
- Record waste (if any)
- Update harvest batch status (finish)
- Testing submission (if required)

## Requirements
- [ ] Metrc API keys (integrator + user)
- [ ] Metrc facility license
- [ ] Google Sheet access (read/write)
- [ ] State-specific endpoint (CA, OR, CO, MI, etc.)

## API Notes
- Batch limit: 10 objects per POST/PUT request
- Use CSV import for bulk data
- JSON for API calls

## Future Enhancements
- [ ] Automated triggers (no manual entry)
- [ ] Real-time inventory sync
- [ ] Compliance reporting auto-generation
- [ ] Extraction schedule based on 45-day rule
