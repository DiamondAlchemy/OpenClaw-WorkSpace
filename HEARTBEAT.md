# HEARTBEAT.md - Mission Pulse

Perform ONLY these checks on each heartbeat. Do NOT extend scope. Do NOT do work that belongs to other agents (Scaramanga/Zorin/Tester for lead enrichment, Vesper/Jaws for GMP, Towelie/Nomi for facility data).

1. Check for unread emails in moneypenny@topsecretworkshops.com. Report count + subjects if any; otherwise stay silent.
2. Check for newly shared files in Google Drive. Report new shares if any; otherwise stay silent.
3. Verify system health only if relevant (e.g., `openclaw doctor` if errors were noted in the prior run). Do NOT run diagnostics speculatively.

**Hard rules:**
- NEVER fabricate data. If you don't run a tool, you have no data — say nothing rather than generate output.
- NEVER run lead enrichment, batch data fetches, or any other agent's workflow. Those agents have their own crons; Moneypenny is NOT a proxy for them.
- If there is nothing to report from items 1–3, respond with `HEARTBEAT_OK` and stop. Silence is correct.
- Every message you send must be backed by a tool call you made in the current turn. No exceptions.
