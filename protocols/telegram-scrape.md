# Telegram Group Scrape Protocol
## For Sub-Agents

**Purpose:** Open a pinned Telegram group, search for specific content, screenshot results, and send back to the requester.

---

## Quick Execute

```bash
cd /Users/m/.openclaw/workspace
./scripts/telegram-scrape.sh "Group Name" "What to search for" "Requester"
```

**Example:**
```bash
./scripts/telegram-scrape.sh "Cannascend" "yields this week" "Diamond"
```

---

## How It Works

1. **Open Telegram** → launches desktop app
2. **Cmd+F** → focuses search bar
3. **Type group name** → starts typing the group
4. **Enter x2** → opens the group (MUST hit twice!)
5. **Cmd+F again** → search within the group
6. **Type search query** → what the requester wants
7. **Screenshot** → captures the results
8. **Send to requester** → via Telegram DM

---

## ⚠️ CRITICAL: Enter Twice!

When opening a group from search results, you MUST press Enter **TWO TIMES**:
- **First Enter:** Selects the group from the dropdown
- **Second Enter:** Opens/enters the group

```bash
peekaboo press enter --count 2
```

---

## Parameters

| Param | Description | Example |
|-------|-------------|---------|
| 1 | Group name (must be pinned at top) | `Cannascend` |
| 2 | What to search for | `yields`, `intake numbers`, `extraction notes` |
| 3 | Who to send results back to | `Diamond`, `Christian`, `Octopussy` |

---

## Alvie's Setup for Speed

- **Pin the group** at the very top of Telegram search results
- **Make the name unique** so it's the first result
- When pinned at top: type name → Enter → directly in group (but still need x2!)

---

## Manual Steps (if script fails)

```bash
# 1. Open Telegram
peekaboo app launch "Telegram"

# 2. Search for group
peekaboo hotkey --keys "cmd,f"
peekaboo type "Cannascend"
peekaboo press enter --count 2  # <-- MUST BE TWICE!
sleep 2

# 3. Search within group
peekaboo hotkey --keys "cmd,f"
peekaboo type "your search query here"
sleep 1

# 4. Screenshot
peekaboo image --mode screen --path /tmp/results.png

# 5. Send to requester
message --action send --channel telegram --target "Diamond" --filePath /tmp/results.png --message "Here are the results"
```

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Wrong group opens | Make sure it's pinned at top |
| Group doesn't open | You're likely hitting Enter only ONCE - must be TWICE |
| Can't find messages | Scroll up manually or check different date range |
| No permissions | `peekaboo permissions` → grant in System Settings |

---

## Usage in Sub-Agent Tasks

When spawning a sub-agent, include the scrape task:

```
Task: Check the Cannascend group for any intake records from last week. Screenshot the relevant messages and send back to Diamond.
```

The sub-agent will run the script with:
- Group: `Cannascend`
- Query: `intake last week` (or whatever finds the info)
- Requester: `Diamond`
