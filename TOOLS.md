# TOOLS.md - Local Notes

## Web Search

Local SearXNG instance (federates Google/Bing/DDG/Brave/Qwant/Startpage) — no rate limits, no CAPTCHAs.

```bash
python3 /Users/m/.openclaw/workspace/scripts/web_search.py "<query>" [--n 10] [--engines google,bing]
```

Returns JSON: `title`, `url`, `snippet`, `engine` per result.

**Do NOT** use the built-in `web_search` tool — it's broken upstream. Always use the script above.


Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin
```

## Actual Setup

### TTS
- Preferred voice: "Moira" (Irish - slightly British, warm, professional)
- Default speaker: Mac mini

### Image Generation
- **nano-banana-pro**: Available for image generation via Gemini 3 Pro
- Config: `skills.nano-banana-pro.env.GEMINI_API_KEY` in openclaw.json
- Command: `uv run /opt/homebrew/lib/node_modules/openclaw/skills/nano-banana-pro/scripts/generate_image.py --prompt "..." --filename "..."`

### Inter-Agent Messaging
- **Script:** `/Users/m/.openclaw/tools/agent_message.py`
- **Usage:** `python3 /Users/m/.openclaw/tools/agent_message.py <agent> "message"`
- **Available agents:** main, octopussy, q, Felix-The_Messenger
- **IMPORTANT:** Use this to message other agents — NOT internal spawns. This sends actual messages via Telegram bots.

### Telegram Bot Accounts
- **main (MoneyPenny):** @MoneyPenny_openclawbot
- **Q:** @Q_topsecret_workshops_bot
- **Octopussy:** @Octopussy_reporter_bot
- **Felix (The Messenger):** @Felix_topsecret_bot

## Installed Skills (ClawHub)

### chart-image (v2.6.35)
Publication-quality charts via Vega-Lite + Sharp. 9 types: line, bar, area, pie, heatmap, candlestick, stacked, multi-series, sparkline. ~200ms/chart, pure Node.js.
- Output: PNG or SVG
- Install: `openclaw skills install chart-image`
- Location: `skills/chart-image/`

### report (v1.0.3)
Recurring scheduled reports with cron + multi-channel delivery (Telegram/email/webhook). User defines data sources and report structure.

### dashboard (v1.0.1)
Static HTML dashboards from data. Dark/light themes, KPI widgets. Cron-driven pipeline.

### notification-system (v1.0.1)
Unified outbound notifications across WhatsApp, Telegram, email. Templates, scheduling, delivery tracking.

### heartbeat (v1.0.1)
Design better HEARTBEAT.md files with adaptive cadence and cron handoffs.

### kpi (v1.0.1)
Track KPIs with targets and execution tracking. Writes to `memory/kpi.md`.

### spreadsheet (v1.0.0)
Read/write/analyze tabular data with schema memory and format preservation.

### fill-docx-template (v1.1.2)
Fill Word `.docx` templates with dynamic data, tables, images. For SOPs, permits, facility docs.

### pdf-form-filler (v0.2.0)
Fill PDF forms programmatically with text/checkboxes. State cannabis manifests.

### document-pro (v1.0.0)
Read/parse/extract PDF, DOCX, PPT key information.

### intake (v1.0.0)
Design intake forms, discovery interviews, onboarding workflows.

### invoice (v1.0.0)
Create/send invoices with automatic numbering, tax calc, payment tracking.

### weekly-report-generator (v1.0.0)
Auto-generate weekly business reports with KPIs, accomplishments, blockers.

---

Add whatever helps you do your job. This is your cheat sheet.
