
## Subagent Permissions (Critical Config)

To allow agents (Octopussy, Q) to spawn subagents, add this to each agent's config:

"subagents": {
  "allowAgents": ["*"]
}

This goes INSIDE the agent definition, NOT in "commands".

Example for Octopussy:
{
  "id": "octopussy",
  "workspace": "/Users/m/.openclaw/workspace-octopussy",
  "subagents": {
    "allowAgents": ["*"]
  },
  ...
}

Last updated: 2026-03-07

