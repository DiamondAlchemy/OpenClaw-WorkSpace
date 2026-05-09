# Security Audit Report — May 9, 2026

**Status: ⚠️ 19 CRITICAL · 5 WARN · 1 INFO**

## CRITICAL Issues

### 1. Open groupPolicy + Elevated Tools Enabled
- Multiple Telegram bot accounts have `groupPolicy="open"` with `tools.elevated` enabled
- A prompt injection in any open group could trigger high-impact command execution
- **Affected:** channels.telegram.groupPolicy and all 18 bot accounts

### 2. Open groupPolicy + Runtime/Filesystem Exposed
- Same open groups have `exec`, `process`, `read`, `write`, `edit`, `apply_patch` tools exposed
- `sandbox=off` on all agents
- `fs.workspaceOnly=false` on defaults (full filesystem access)
- **Affected:** All 18 agents including defaults

### 3. Telegram Open Groups with No Allowlist
- `channels.telegram.groupPolicy="open"` with no `channels.telegram.groups` allowlist
- Any Telegram group can add and ping the bots
- Multiple warnings: warning.1 through warning.20

### 4. Telegram Group Commands Have No Sender Allowlist
- `groupAllowFrom` not configured
- Any group member can invoke `/…` commands

## WARNINGS

- `autoAllowSkills` enabled for exec approvals (widens host exec trust)
- `gpt-4o-mini` in fallback models (below recommended tier)
- lossless-claw plugin tools reachable under permissive policy
- Unpinned npm spec: `@openclaw/voice-call`

## Recommendations

1. Add `channels.telegram.groupAllowFrom` to restrict which groups can ping bots
2. Set `tools.fs.workspaceOnly=true` for exposed agents
3. Enable sandbox mode for agents handling group input
4. Consider allowlist mode for groupPolicy if group access is meant to be restricted

---
*Audit run: 2026-05-09 14:00 UTC*
