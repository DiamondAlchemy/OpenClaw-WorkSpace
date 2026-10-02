import json, sys

d = json.load(sys.stdin)
print("critical:", d["summary"]["critical"])
print("warn:", d["summary"]["warn"])
print("info:", d["summary"]["info"])
print("deep_gateway:", json.dumps(d.get("deep", {}), indent=2))
print("secretDiagnostics:", d.get("secretDiagnostics"))
print("---FINDINGS---")
for i, f in enumerate(d.get("findings", []), 1):
    sev = f.get("severity")
    cid = f.get("checkId")
    print(f"\n[{i}] severity={sev} checkId={cid}")
    print("title:", f.get("title"))
    print("detail:")
    print(f.get("detail", ""))
    if f.get("remediation"):
        print("remediation:", f.get("remediation"))
