# Inter-Agent Communication

Agents communicate via shared file system. No Telegram routing needed.

## Shared Folder
`/Users/m/.openclaw/workspace/shared/`

## How It Works

### Receiving Messages
At session start, check your inbox for new messages:
```
ls /Users/m/.openclaw/workspace/shared/inbox/
```

Read any messages addressed to you:
```
cat /Users/m/.openclaw/workspace/shared/inbox/[filename]
```

### Sending Messages
To message another agent or human:
1. Write your message to the outbox:
```
/Users/m/.openclaw/workspace/shared/outbox/[recipient]-[timestamp].md
```

2. The receiving agent will check their inbox at session start.

### Message Format
```markdown
# From: [sender]
# To: [recipient] (agentId or "Alvie" / "Christian")
# Time: [ISO timestamp]

[Your message here]
```

## Recipients
- `moneypenny` - MoneyPenny (orchestrator)
- `octopussy` - Octopussy (reporter)
- `q` - Q (data manager)
- `Alvie` - Alvaro Medina
- `Christian` - Christian Sutton
