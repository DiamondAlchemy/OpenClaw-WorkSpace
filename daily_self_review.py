
import os
import sys
import subprocess
import shlex
from datetime import datetime, timedelta

# Define base directories
WORKSPACE_DIR = "/Users/m/.openclaw/workspace"
REFERENCE_DIR = os.path.join(WORKSPACE_DIR, "reference")
MEMORY_DIR = os.path.join(WORKSPACE_DIR, "memory")

def read_file(filepath):
    """Safely reads a file and returns its content or an error string."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading {filepath}: {e}"

def find_markdown_files(directory):
    """Finds all .md files in a directory, excluding reference files."""
    md_files = []
    for root, _, files in os.walk(directory):
        if root.startswith(MEMORY_DIR):  # Skip the memory directory for this function
            continue
        for file in files:
            if file.endswith(".md"):
                full_path = os.path.join(root, file)
                # Exclude the reference guides themselves from the check
                if not full_path.startswith(REFERENCE_DIR):
                    md_files.append(full_path)
    return md_files

def analyze_recent_lessons(days=7):
    """Scans recent memory logs for key operational lessons."""
    lessons_found = []
    keywords = ["mistake", "error", "failure", "lesson learned"]
    today = datetime.now()

    for i in range(days):
        date_to_check = today - timedelta(days=i)
        log_filename = date_to_check.strftime("%Y-%m-%d.md")
        log_filepath = os.path.join(MEMORY_DIR, log_filename)

        if os.path.exists(log_filepath):
            content = read_file(log_filepath)
            if not content.startswith("File not found"):
                for line_num, line in enumerate(content.splitlines(), 1):
                    if any(keyword in line.lower() for keyword in keywords):
                        lessons_found.append(f"- {log_filename}, line {line_num}: {line.strip()}")
    
    if not lessons_found:
        return "No specific lessons from mistakes, errors, or failures found in the last 7 days."
    else:
        return "The following potential lessons were identified from recent memory logs:\n" + "\n".join(lessons_found)


def analyze_against_best_practices(filepath, openclaw_guide, anthropic_guide):
    """Uses the Gemini CLI to analyze a file against best practices guides."""
    file_content = read_file(filepath)
    if file_content.startswith("File not found") or file_content.startswith("Error reading"):
        return f"Could not read {filepath} for analysis."

    # Use a concise, clear prompt for the LLM
    prompt = f"""
    You are a configuration auditor. Your task is to check if a user's configuration file violates any best practices.
    You will be given two guides for best practices and one user configuration file.
    Your analysis should be strict and focused only on direct contradictions or clear deviations from the guides. Do not comment on style.

    Here is the OpenClaw Best Practices Guide:
    <guide_openclaw>
    {openclaw_guide}
    </guide_openclaw>

    Here is the Anthropic Prompting Guide:
    <guide_anthropic>
    {anthropic_guide}
    </guide_anthropic>

    Now, analyze the following user configuration file:
    <config_file filename="{os.path.basename(filepath)}">
    {file_content}
    </config_file>

    Please list any violations or contradictions you find. If you find no issues, respond with "No contradictions found."
    """

    try:
        # Using gemini CLI tool. Ensure it is in the system's PATH.
        # shlex.quote is crucial for safely passing the prompt as a single argument.
        command = f"gemini -m gemini-2.5-flash {shlex.quote(prompt)}"
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "Error: The 'gemini' command was not found. Please ensure the Gemini CLI is installed and in the system PATH."
    except subprocess.CalledProcessError as e:
        return f"Error during Gemini CLI execution for {filepath}: {e.stderr}"
    except Exception as e:
        return f"An unexpected error occurred during analysis of {filepath}: {e}"


def generate_review_summary():
    """Generates the full daily self-review report."""
    summary_parts = ["Daily Self-Review & Best Practices Audit:"]

    # 1. Load the reference guides
    openclaw_guide = read_file(os.path.join(REFERENCE_DIR, "openclaw_best_practices.md"))
    anthropic_guide = read_file(os.path.join(REFERENCE_DIR, "anthropic_prompting_guide.md"))

    if openclaw_guide.startswith("File not found") or anthropic_guide.startswith("File not found"):
        summary_parts.append("--- AUDIT FAILED ---")
        summary_parts.append("Could not find one or both reference guides. Aborting best practices audit.")
        if openclaw_guide.startswith("File not found"): summary_parts.append(f"- {openclaw_guide}")
        if anthropic_guide.startswith("File not found"): summary_parts.append(f"- {anthropic_guide}")
        # Still run the lessons learned part
        summary_parts.append("\n--- Recent Lessons ---")
        summary_parts.append(analyze_recent_lessons())
        summary_parts.append("\n--- End of Report ---")
        return "\n".join(summary_parts)

    # 2. Find and analyze all workspace markdown files
    summary_parts.append("\n--- Best Practices Audit ---")
    md_files_to_check = find_markdown_files(WORKSPACE_DIR)

    if not md_files_to_check:
        summary_parts.append("No markdown configuration files found to audit.")
    else:
        for filepath in md_files_to_check:
            filename = os.path.basename(filepath)
            summary_parts.append(f"\n[+] Auditing: {filename}")
            analysis_result = analyze_against_best_practices(filepath, openclaw_guide, anthropic_guide)
            summary_parts.append(analysis_result)
            
    # 3. Analyze recent lessons
    summary_parts.append("\n--- Recent Lessons ---")
    summary_parts.append(analyze_recent_lessons())

    summary_parts.append("\n--- End of Report ---")
    return "\n".join(summary_parts)


TELEGRAM_MSG_LIMIT = 4000  # Telegram max is 4096, leave buffer


def truncate_for_telegram(text, limit=TELEGRAM_MSG_LIMIT):
    """Truncate output to fit Telegram's message limit."""
    if len(text) <= limit:
        return text
    # Find a good cutoff point
    truncated = text[:limit]
    # Try to cut at last newline for clean output
    last_newline = truncated.rfind("\n")
    if last_newline > limit * 0.8:
        truncated = truncated[:last_newline]
    truncated += "\n\n... [truncated — full report exceeds Telegram limit]"
    return truncated


if __name__ == "__main__":
    # This check ensures we don't run the full script if just imported.
    report = generate_review_summary()
    print(truncate_for_telegram(report))
