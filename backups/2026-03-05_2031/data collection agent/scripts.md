# Scripts

**STATUS: PENDING TRAINING**

These scripts define the exact conversation flow for each call type. Until training is complete, do not attempt to collect data.

## Script Types

### 1. Intake Report
- Triggers when material arrives at facility
- Collects: Batch ID, Material Type, Weight, Vendor, Cultivar, Date/Time

### 2. Extraction Start
- Triggers when opening a new run
- Collects: Batch ID, Start Time, Biomass Input, Butane Lot, Operator, Recipe

### 3. Extraction End / Yield Report
- Triggers when extraction run completes
- Collects: Batch ID, End Time, Pre-Purge Weight, solvent recovery, notes

### 4. Post Processing Report
- Triggers when batch finishing is complete
- Collects: Batch ID, Post-Purge Weight, Residual Solvent, jarred weight, final yield

### 5. Issue / Downtime Report
- Triggers when any problem occurs
- Collects: Batch ID (if applicable), Issue Type, Description, Resolution, Downtime

---

## Script Training Checklist
- [ ] Intake Report script finalized
- [ ] Extraction Start script finalized
- [ ] Extraction End script finalized
- [ ] Post Processing script finalized
- [ ] Issue Report script finalized
- [ ] All formats validated against Google Sheet columns
- [ ] Test conversations completed successfully
- [ ] Owner sign-off received

---

*(Scripts to be added after training)*
