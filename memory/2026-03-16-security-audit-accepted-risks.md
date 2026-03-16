# Security Audit - Accepted Risks

All security audit items below are documented as accepted risks:

## Current Audit (March 16, 2026)

### Critical (7) - Accepted Risk
- **groupPolicy="open" + elevated tools**: Intentional. Security boundary is `allowFrom` lists.
- **groupPolicy="open" + runtime/filesystem**: Intentional. Security boundary is `allowFrom` lists.
- **5× Telegram warnings**: Same as above — allowFrom controls access.
- **Plugin tools exposure (lossless-claw)**: Trusted plugin, intentional.
- **Code safety issue at src/engine.ts:2**: Reviewed, not a real risk.
- **Gateway probe failed (missing scope)**: Non-blocking warning.

### Warnings (2) - Accepted Risk
- **Multi-user setup detected**: Expected — Diamond & Christian both use the system
- **Plugin tools under permissive policy**: lossless-claw is trusted

### Info (1)
- **Attack surface summary**: Known, managed

---

## Previous Acceptances (March 15, 2026)

Same items accepted as documented above.

---

## Agent Workspace Lockdown (March 16, 2026)

- Main agent (MoneyPenny): `workspaceOnly: true` — locked down to own workspace
- Other agents already had this setting
- Unlocking requires explicit permission from Diamond
