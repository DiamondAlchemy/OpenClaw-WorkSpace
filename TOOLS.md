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

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
