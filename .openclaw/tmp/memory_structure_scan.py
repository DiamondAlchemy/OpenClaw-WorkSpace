from pathlib import Path
from collections import Counter

p = Path("/Users/m/.openclaw/workspace/MEMORY.md")
text = p.read_text(encoding="utf-8", errors="replace")
lines = text.splitlines()
print(f"exists=yes lines={len(lines)} bytes={p.stat().st_size}")
print("first_12_redacted:")
for i, l in enumerate(lines[:12], 1):
    shown = l[:160]
    low = l.lower()
    if "token" in low or "key" in low or "secret" in low:
        shown = "[REDACTED-POSSIBLE-SECRET]"
    print(f"{i:04d}|{shown}")
print("last_20:")
start = max(1, len(lines) - 19)
for i, l in enumerate(lines[-20:], start):
    shown = l[:180]
    low = l.lower()
    if "token" in low or "key" in low or "secret" in low:
        shown = "[REDACTED-POSSIBLE-SECRET]"
    print(f"{i:04d}|{shown}")
print("---heading_inventory---")
heads = []
tab_lines = []
conflict = []
for i, l in enumerate(lines, 1):
    if l.startswith("#"):
        heads.append((i, l[:200]))
    if "\t" in l:\n        tab_lines.append(i)\n    if l.startswith("<<<<<<<") or l.startswith(">>>>>>>") or l.startswith("======="):
        conflict.append(i)
print(f"heading_count={len(heads)}")
for i, h in heads:
    print(f"{i:04d}|{h}")
c = Counter(h for _, h in heads)
dups = [(h, n) for h, n in c.items() if n > 1]
print(f"duplicate_headings={len(dups)}")
for h, n in dups:
    print(f"DUP x{n}|{h}")
empty = [(i, h) for i, h in heads if h.strip("#").strip() == ""]
print(f"empty_headings={len(empty)}")
long = [(i, len(l)) for i, l in enumerate(lines, 1) if len(l) > 500]
print(f"lines_over_500_chars={len(long)}")
for i, n in long[:15]:
    print(f"long {i} chars={n}")
print("null_bytes", "\x00" in text)
run = 0
maxrun = 0
runstarts = []
for i, l in enumerate(lines, 1):
    if l.strip() == "":
        run += 1
        maxrun = max(maxrun, run)
        if run == 6:
            runstarts.append(i - 5)
    else:
        run = 0
print(f"max_consecutive_blank={maxrun} long_blank_run_starts={runstarts[:10]}")
print(f"tab_count={len(tab_lines)} conflict_markers={conflict}")
levels = Counter(len(h) - len(h.lstrip("#")) for _, h in heads)
print("heading_levels", dict(levels))
for needle in ["TODO", "FIXME", "TBD", "PLACEHOLDER", "<<<<<<<"]:
    hits = [i for i, l in enumerate(lines, 1) if needle.lower() in l.lower()]
    if hits:
        print(f"{needle} lines={hits[:10]}")
print("---section_sizes---")
if heads:
    idxs = [i for i, _ in heads] + [len(lines) + 1]
    for a, b, h in zip(idxs, idxs[1:], [h for _, h in heads]):
        print(f"{a:04d}-{b-1:04d} n={b-a:4d} {h}")
print("---secret_line_flags---")
for i, l in enumerate(lines, 1):
    low = l.lower()
    if any(x in low for x in ["token", "api_key", "apikey", "secret", "password", "bearer "]):
        print(f"secretish_line={i} len={len(l)}")
