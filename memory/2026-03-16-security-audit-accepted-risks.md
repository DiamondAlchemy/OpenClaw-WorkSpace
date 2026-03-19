# Security Audit - Accepted Risks

All security audit items below are documented as accepted risks:

## Current Audit (March 19, 2026) - DISMISSED

### Dismissed Issues (Same recurring issues)
- groupPolicy="open" + elevated tools — allowFrom lists are the security boundary
- groupPolicy="open" + runtime/filesystem — intentional, allowFrom controls access
- 5× Telegram warnings — same root cause, allowFrom configured
- Plugin tools exposure (lossless-claw) — false positive, LCM compaction engine
- Gateway probe failed (missing scope) — non-blocking warning
- Multi-user setup — expected for Top Secret Workshops
- Extension plugin tools under permissive policy — trusted plugins

### Action Taken
- **DISMISSED** as recurring accepted risks
- Next audit: Expect same issues to appear

---

## Current Audit (March 18, 2026) - DISMISSED

### Dismissed Issues (Same as March 16 & March 15)
- groupPolicy="open" + elevated tools — allowFrom lists are the security boundary
- groupPolicy="open" + runtime/filesystem — intentional, allowFrom controls access
- 5× Telegram warnings — same root cause, allowFrom configured
- Plugin tools exposure (lossless-claw) — false positive, LCM compaction engine
- Gateway probe failed (missing scope) — non-blocking warning
- Multi-user setup — expected for Top Secret Workshops
- Extension plugin tools under permissive policy — trusted plugins

### Action Taken
- **DISMISSED** as recurring accepted risks
- Next audit: Expect same issues to appear

---

## Previous Acceptances

### March 16, 2026 - Accepted Risk
Same issues as above, documented and accepted.

### March 15, 2026 - Accepted Risk  
First round of accepting these issues as documented risks.

### March 4, 2024 - Addressed
- Dangerous node commands (camera.snap, screen.record) — addressed

---

## Agent Workspace Lockdown (March 16, 2026)

- Main agent (MoneyPenny): `workspaceOnly: true` — locked down to own workspace
- Other agents already had this setting
- Unlocking requires explicit permission from Diamond
