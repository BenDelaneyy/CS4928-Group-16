"""
Event A: check whether the original data package contains issue histories for the 7 projects
missing from Data/*/issue_history/ (Week 9 decision: check the original data package first).
Standard library only. Run from the repository root:  python evidence/event_a/data_package_check.py
Writes evidence/event_a/data_package_check_<YYYYMMDD>.txt
"""
import datetime
import os
import zipfile

ARCHIVES = ["Data/projects.zip", "Data/analyzedDataset.zip"]
MISSING = ["nymtech#nym", "SrinivasanTarget#ContractTestingBoilerplate", "topcoder-platform#tc-project-service",
        "ZeroCater#zc_events", "rero#rero-mef", "shlinkio#shlink", "cofacts#rumors-api"]

now = datetime.datetime.now()
out_path = f"evidence/event_a/data_package_check_{now:%Y%m%d}.txt"
lines = [f"Event A data package check - {now:%Y-%m-%d %H:%M:%S}",
        "Script: evidence/event_a/data_package_check.py",
        "Search: every archive entry name, case-insensitive, for 'issue_history', for each full project name",
        "(owner#repo) and for each owner/repo pair written with '/'.", ""]

for archive in ARCHIVES:
    with zipfile.ZipFile(archive) as z:
        names = z.namelist()
    lower = [n.lower() for n in names]
    lines.append(f"{archive}: {len(names)} entries, {os.path.getsize(archive)} bytes")
    hits = [n for n, l in zip(names, lower) if "issue_history" in l]
    lines.append(f"  entries containing 'issue_history': {len(hits)}")
    for project in MISSING:
        owner, repo = project.split("#")
        keys = [project.lower(), f"{owner}/{repo}".lower()]
        found = [n for n, l in zip(names, lower) if any(k in l for k in keys)]
        lines.append(f"  {project}: {len(found)} matching entries" + "".join(f"\n    {f}" for f in found))
    lines.append("")

lines.append("Conclusion: an issue history for a project exists in an archive only if it is listed above.")
with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
print(f"> wrote {out_path}")
