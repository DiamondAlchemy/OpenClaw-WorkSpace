# Telegram Group Scrape Protocol
## For Gemini Sub-Agents (Vision-Enabled)

**Purpose:** Open a pinned Telegram group, screenshot the chat, and send to requester.

---

## ⚠️ CRITICAL: Enter Twice!

When opening a group from search results, you MUST press Enter **TWO TIMES**:
- **First Enter:** Selects the group from the dropdown
- **Second Enter:** Opens/enters the group

```bash
peekaboo press enter --count 2
```

---

## Steps for Sub-Agent

### Step 1: Open Telegram & Navigate to Group

```bash
# Open Telegram
peekaboo app launch "Telegram"
peekaboo sleep 2000

# Search for group
peekaboo hotkey --keys "cmd,f"
peekaboo type "Cannascend"
peekaboo sleep 1000

# Enter group - MUST BE TWICE!
peekaboo press enter --count 2
peekaboo sleep 2000

# Find #General subtopic
peekaboo hotkey --keys "cmd,f"
peekaboo type "#General"
peekaboo press enter
peekaboo sleep 1500
```

### Step 2: Screenshot

```bash
peekaboo image --mode screen --path /Users/m/.openclaw/workspace/telegram-scrape.png
```

### Step 3: Send to Requester (Use Message Tool!)

Do NOT use the `message` command in bash. Use the **message tool** directly:

```
action: send
channel: telegram
target: "Diamond" (or whoever the requester is)
filePath: /Users/m/.openclaw/workspace/telegram-scrape.png
message: "Cannascend #General screenshot"
```

---

## Example Task Prompt

When spawning this sub-agent, use:

```
Task: Screenshot the Cannascend #General chat and send to Diamond.

1. Open Telegram → search "Cannascend" → Enter x2 → find #General
2. Screenshot to /Users/m/.openclaw/workspace/telegram-scrape.png
3. Send via message tool to Diamond
```

---

## Parameters

| Item | Value |
|------|-------|
| Group | Cannascend |
| Subtopic | #General |
| Screenshot path | `/Users/m/.openclaw/workspace/telegram-scrape.png` |
| Requester | Diamond (Telegram: 8217045820) |
