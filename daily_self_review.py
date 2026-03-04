
import os
import sys

# Define the base workspace directory for relative paths
WORKSPACE_DIR = "/Users/m/.openclaw/workspace"
SKILLS_DIR = "/opt/homebrew/lib/node_modules/openclaw/skills"

def read_file(filepath):
    try:
        with open(filepath, 'r') as f:
            return f.read()
    except FileNotFoundError:
        return f"File not found: {filepath}"
    except Exception as e:
        return f"Error reading {filepath}: {e}"

def scan_for_markers(content):
    markers = []
    for i, line in enumerate(content.splitlines()):
        if "TODO" in line:
            markers.append(f"TODO (line {i+1}): {line.strip()}")
        if "FIXME" in line:
            markers.append(f"FIXME (line {i+1}): {line.strip()}")
    return markers

def summarize_skills(skills_dir):
    try:
        if not os.path.exists(skills_dir):
            return f"Skills directory not found: {skills_dir}"
        skill_names = [d for d in os.listdir(skills_dir) if os.path.isdir(os.path.join(skills_dir, d))]
        return f"Found {len(skill_names)} skills: {', '.join(skill_names)}"
    except Exception as e:
        return f"Error listing skills: {e}"

def generate_review_summary():
    summary_parts = ["Daily Self-Review Report:"]

    # Read core files
    files_to_review = {
        "MEMORY.md": os.path.join(WORKSPACE_DIR, "MEMORY.md"),
        "SOUL.md": os.path.join(WORKSPACE_DIR, "SOUL.md"),
        "IDENTITY.md": os.path.join(WORKSPACE_DIR, "IDENTITY.md"),
        "AGENTS.md": os.path.join(WORKSPACE_DIR, "AGENTS.md")
    }

    for filename, filepath in files_to_review.items():
        content = read_file(filepath)
        summary_parts.append(f"--- {filename} ---")
        if content.startswith("File not found") or content.startswith("Error reading"):
            summary_parts.append(content)
        else:
            markers = scan_for_markers(content)
            if markers:
                summary_parts.append("Potential areas for review:")
                for marker in markers:
                    summary_parts.append(f"  - {marker}")
            else:
                summary_parts.append("No explicit 'TODO' or 'FIXME' markers found.")
        summary_parts.append("")

    # Review skills directory
    skills_summary = summarize_skills(SKILLS_DIR)
    summary_parts.append(f"--- Skills Directory ---")
    summary_parts.append(skills_summary)
    summary_parts.append("")

    summary_parts.append("End of Daily Self-Review Report.")
    return "\n".join(summary_parts) # Use \n for cron job output that will be passed as string

if __name__ == "__main__":
    print(generate_review_summary())
