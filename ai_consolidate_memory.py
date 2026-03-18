#!/usr/bin/env python3
"""
ai_consolidate_memory.py — AI-powered memory consolidation for OpenClaw agents.

Reads daily memory logs, sends them to an LLM for intelligent summarization,
and writes a distilled MEMORY.md with only essential facts, decisions, and context.

Usage:
    python3 ai_consolidate_memory.py                          # Main workspace, MiniMax (default)
    python3 ai_consolidate_memory.py --workspace /path/to/ws  # Specific workspace
    python3 ai_consolidate_memory.py --max-lines 300          # Custom cap
    python3 ai_consolidate_memory.py --dry-run                # Preview without writing
    python3 ai_consolidate_memory.py --days 7                 # Only last 7 days of logs
    python3 ai_consolidate_memory.py --provider anthropic     # Use Claude instead of MiniMax

Supports: MiniMax M2.5 (default), Anthropic Claude, Google Gemini
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timedelta

try:
    import anthropic
except ImportError:
    print("ERROR: anthropic package not installed. Run: pip3 install anthropic")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
DEFAULT_WORKSPACE = "/Users/m/.openclaw/workspace"
DEFAULT_MAX_LINES = 400
CHUNK_TOKEN_LIMIT = 80000  # stay well under context window per chunk
CHARS_PER_TOKEN_EST = 4

PROVIDERS = {
    "minimax": {
        "base_url": "https://api.minimax.io/anthropic",
        "model": "MiniMax-M2.5-highspeed",
        "auth_source": "minimax-oauth",  # load from auth-profiles.json
    },
    "anthropic": {
        "base_url": None,  # default Anthropic endpoint
        "model": "claude-sonnet-4-20250514",
        "auth_source": "env",  # ANTHROPIC_API_KEY
    },
    "gemini": {
        "base_url": "https://generativelanguage.googleapis.com/v1beta/",
        "model": "gemini-2.5-flash",
        "auth_source": "env-gemini",  # GEMINI_API_KEY
    },
}

CONSOLIDATION_PROMPT = """You are a memory consolidation engine for an AI agent called MoneyPenny.

Your job is to distill raw daily session logs into a clean, structured long-term memory file.

RULES:
1. Extract ONLY information worth remembering across sessions:
   - Decisions made (who decided what, when, and why)
   - Facts about the system, people, processes, or business
   - Configuration changes and their reasons
   - Bugs found and how they were fixed (one-liner each)
   - Strategy results and key findings (numbers matter — keep them)
   - Operational protocols and procedures established
   - Contact info, credentials, account details mentioned
   - Pending/open items that haven't been resolved

2. DISCARD:
   - Raw conversation back-and-forth / chat transcripts
   - Telegram/WhatsApp metadata (sender JSON, message IDs, session IDs)
   - Greetings, banter, emoji reactions, filler
   - Step-by-step troubleshooting that led nowhere
   - Duplicate information (keep the most recent/complete version)
   - Temporary states that have since been resolved

3. FORMAT:
   - Use markdown with clear section headings by topic (not by date)
   - Within each section, entries should be newest-first
   - Tag each entry with its date: [YYYY-MM-DD]
   - Use concise bullet points, not paragraphs
   - Keep tables if the data is tabular (strategy results, etc.)
   - Total output MUST be under {max_lines} lines

4. SECTIONS to use (only include sections that have content):
   - ## System & Configuration
   - ## People & Contacts
   - ## Operational Protocols
   - ## Business Operations (Cannabis/TSW)
   - ## Crypto & Trading
   - ## Agent Ecosystem
   - ## Bugs & Fixes
   - ## Pending / Open Items

5. At the top, include a metadata block:
   ```
   > **Last consolidated:** {timestamp}
   > **Source:** {num_logs} daily logs ({date_range})
   > **Method:** AI-powered consolidation (ai_consolidate_memory.py)
   ```
"""

CHUNK_PROMPT = """Here are daily memory logs to consolidate. Extract the essential information following the rules above.

Return ONLY the distilled content (markdown). No preamble, no explanation.

--- LOGS START ---
{chunk}
--- LOGS END ---"""

MERGE_PROMPT = """You have multiple consolidated chunks from different time periods. Merge them into a single, unified MEMORY.md.

RULES:
- Deduplicate across chunks (keep the most recent/complete version)
- Organize by topic section, not chronologically
- Newest information first within each section
- Total output MUST be under {max_lines} lines
- Preserve all dates, numbers, and specific details

--- CHUNKS START ---
{chunks}
--- CHUNKS END ---

Return ONLY the final merged markdown. No preamble."""


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
def load_minimax_token():
    """Load MiniMax OAuth access token from auth-profiles.json."""
    auth_path = Path("/Users/m/.openclaw/agents/main/agent/auth-profiles.json")
    if auth_path.exists():
        try:
            data = json.loads(auth_path.read_text())
            profiles = data.get("profiles", data)

            # Prefer minimax-portal OAuth token
            portal = profiles.get("minimax-portal:default", {})
            if portal.get("access"):
                return portal["access"]

            # Fallback: minimax service account key
            svc = profiles.get("minimax:default", {})
            if svc.get("key"):
                return svc["key"]
        except (json.JSONDecodeError, KeyError):
            pass

    print("ERROR: No MiniMax token found in auth-profiles.json")
    sys.exit(1)


def load_api_key(provider: str):
    """Load API key for the given provider."""
    if provider == "minimax":
        return load_minimax_token()

    if provider == "anthropic":
        key = os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            config_path = Path("/Users/m/.openclaw/openclaw.json")
            if config_path.exists():
                try:
                    config = json.loads(config_path.read_text())
                    key = config.get("env", {}).get("ANTHROPIC_API_KEY")
                except (json.JSONDecodeError, KeyError):
                    pass
        if key:
            return key
        print("ERROR: No ANTHROPIC_API_KEY found")
        sys.exit(1)

    if provider == "gemini":
        key = os.environ.get("GEMINI_API_KEY")
        if not key:
            config_path = Path("/Users/m/.openclaw/openclaw.json")
            if config_path.exists():
                try:
                    config = json.loads(config_path.read_text())
                    key = config.get("env", {}).get("GEMINI_API_KEY")
                except (json.JSONDecodeError, KeyError):
                    pass
        if key:
            return key
        print("ERROR: No GEMINI_API_KEY found")
        sys.exit(1)

    print(f"ERROR: Unknown provider '{provider}'")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def find_daily_logs(memory_dir: Path, days: int = None) -> list[Path]:
    """Find daily log files, optionally filtered to last N days."""
    if not memory_dir.exists():
        print(f"ERROR: {memory_dir} not found")
        sys.exit(1)

    all_logs = sorted(memory_dir.glob("*.md"))
    if not all_logs:
        print(f"ERROR: No .md files in {memory_dir}")
        sys.exit(1)

    if days:
        cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        all_logs = [f for f in all_logs if f.stem >= cutoff or not f.stem[0].isdigit()]

    return all_logs


def read_logs(log_files: list[Path]) -> list[dict]:
    """Read all log files into structured dicts."""
    logs = []
    for f in log_files:
        try:
            content = f.read_text(encoding="utf-8")
            logs.append({
                "filename": f.name,
                "date": f.stem,
                "content": content,
                "chars": len(content),
            })
        except Exception as e:
            print(f"  WARNING: Could not read {f.name}: {e}")
    return logs


def chunk_logs(logs: list[dict], max_chars: int) -> list[str]:
    """Split logs into chunks that fit within the token limit."""
    chunks = []
    current_chunk = []
    current_chars = 0

    for log in logs:
        if log["chars"] > max_chars:
            if current_chunk:
                chunks.append("\n\n---\n\n".join(current_chunk))
                current_chunk = []
                current_chars = 0
            chunks.append(f"## Log: {log['filename']}\n\n{log['content'][:max_chars]}\n\n[...truncated]")
            continue

        if current_chars + log["chars"] > max_chars:
            chunks.append("\n\n---\n\n".join(current_chunk))
            current_chunk = []
            current_chars = 0

        current_chunk.append(f"## Log: {log['filename']}\n\n{log['content']}")
        current_chars += log["chars"]

    if current_chunk:
        chunks.append("\n\n---\n\n".join(current_chunk))

    return chunks


def call_llm(client, prompt: str, system: str, model: str, max_tokens: int = 4096) -> str:
    """Send a prompt to the LLM via Anthropic-compatible API."""
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    # Extract text from response, skipping thinking blocks
    for block in response.content:
        if hasattr(block, "text"):
            return block.text
    # Fallback: stringify first block
    return str(response.content[0])


def backup_memory(memory_file: Path):
    """Backup existing MEMORY.md with timestamp."""
    if memory_file.exists():
        backup_dir = memory_file.parent / "backups" / "MEMORY"
        backup_dir.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = backup_dir / f"MEMORY.md.backup-{ts}"
        shutil.copy2(memory_file, backup_path)
        print(f"  Backed up → {backup_path.name}")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="AI-powered memory consolidation")
    parser.add_argument("--workspace", default=DEFAULT_WORKSPACE, help="Workspace path")
    parser.add_argument("--max-lines", type=int, default=DEFAULT_MAX_LINES, help="Max lines in output")
    parser.add_argument("--days", type=int, default=None, help="Only process last N days of logs")
    parser.add_argument("--dry-run", action="store_true", help="Print output, don't write")
    parser.add_argument("--provider", default="minimax", choices=["minimax", "anthropic", "gemini"],
                        help="LLM provider (default: minimax)")
    parser.add_argument("--model", default=None, help="Override model name")
    args = parser.parse_args()

    provider_config = PROVIDERS[args.provider]
    model = args.model or provider_config["model"]
    base_url = provider_config["base_url"]

    workspace = Path(args.workspace)
    memory_dir = workspace / "memory"
    memory_file = workspace / "MEMORY.md"
    max_chars = CHUNK_TOKEN_LIMIT * CHARS_PER_TOKEN_EST

    print(f"OpenClaw AI Memory Consolidation")
    print(f"  Workspace: {workspace}")
    print(f"  Provider: {args.provider}")
    print(f"  Model: {model}")
    print(f"  Max lines: {args.max_lines}")
    if args.days:
        print(f"  Window: last {args.days} days")
    print()

    # 1. Load logs
    log_files = find_daily_logs(memory_dir, args.days)
    logs = read_logs(log_files)
    total_chars = sum(l["chars"] for l in logs)
    print(f"  Found {len(logs)} logs ({total_chars:,} chars total)")

    # 2. Chunk
    chunks = chunk_logs(logs, max_chars)
    print(f"  Split into {len(chunks)} chunks for processing")
    print()

    # 3. Init client
    api_key = load_api_key(args.provider)

    client_kwargs = {"api_key": api_key}
    if base_url:
        client_kwargs["base_url"] = base_url

    client = anthropic.Anthropic(**client_kwargs)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_range = f"{logs[0]['date']} to {logs[-1]['date']}" if len(logs) > 1 else logs[0]["date"]

    system_prompt = CONSOLIDATION_PROMPT.format(
        max_lines=args.max_lines,
        timestamp=timestamp,
        num_logs=len(logs),
        date_range=date_range,
    )

    # 4. Process chunks
    consolidated_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"  Processing chunk {i + 1}/{len(chunks)} ({len(chunk):,} chars)...")
        prompt = CHUNK_PROMPT.format(chunk=chunk)
        result = call_llm(client, prompt, system_prompt, model=model, max_tokens=4096)
        consolidated_chunks.append(result)
        print(f"    → {len(result.splitlines())} lines extracted")

    # 5. Merge if multiple chunks
    if len(consolidated_chunks) > 1:
        print(f"\n  Merging {len(consolidated_chunks)} chunks...")
        merge_input = "\n\n===CHUNK BOUNDARY===\n\n".join(consolidated_chunks)
        merge_prompt = MERGE_PROMPT.format(
            max_lines=args.max_lines,
            chunks=merge_input,
        )
        final = call_llm(client, merge_prompt, system_prompt, model=model, max_tokens=8192)
    else:
        final = consolidated_chunks[0]

    # 6. Add header if not present (avoid duplication if LLM already included it)
    if not final.lstrip().startswith("# MEMORY"):
        header = (
            f"# MEMORY — Consolidated Knowledge Base\n\n"
            f"> **Last consolidated:** {timestamp}\n"
            f"> **Source:** {len(logs)} daily logs ({date_range})\n"
            f"> **Method:** AI-powered consolidation (ai_consolidate_memory.py)\n\n"
            f"---\n\n"
        )
        final = header + final
    else:
        # LLM included its own header — make sure metadata is accurate
        final = (
            f"# MEMORY — Consolidated Knowledge Base\n\n"
            f"> **Last consolidated:** {timestamp}\n"
            f"> **Source:** {len(logs)} daily logs ({date_range})\n"
            f"> **Method:** AI-powered consolidation (ai_consolidate_memory.py)\n\n"
            f"---\n\n"
            + final.split("---", 1)[-1].lstrip("\n")
        )

    line_count = len(final.splitlines())
    print(f"\n  Final output: {line_count} lines")

    if line_count > args.max_lines:
        print(f"  WARNING: Output exceeds {args.max_lines} line cap ({line_count} lines)")
        print(f"  Consider reducing --days or running again")

    # 7. Write or print
    if args.dry_run:
        print("\n" + "=" * 60)
        print("DRY RUN — Would write:\n")
        print(final)
    else:
        backup_memory(memory_file)
        memory_file.write_text(final, encoding="utf-8")
        print(f"\n  Wrote {memory_file} ({line_count} lines)")

    print("\nDone.")


if __name__ == "__main__":
    main()
