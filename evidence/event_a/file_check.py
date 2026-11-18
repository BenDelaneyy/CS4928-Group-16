"""
Event A: check that the commit file and the issue-history file exist for each of the 12 sampled projects.
Same columns as evidence/event_a/event_a_file_check_20261030_083437.csv. Standard library only.
Run from the repository root:  python evidence/event_a/file_check.py
Writes evidence/event_a/event_a_file_check_<YYYYMMDD_HHMMSS>.csv
"""
import csv
import datetime
import os

SAMPLE = "Data/final_data_file_sample.csv"
FOLDER = {"MS": "Data/cases", "~MS": "Data/controls"}

out_path = f"evidence/event_a/event_a_file_check_{datetime.datetime.now():%Y%m%d_%H%M%S}.csv"
with open(SAMPLE, newline="", encoding="utf-8") as f:
    rows = list(csv.DictReader(f))

with open(out_path, "w", newline="\n", encoding="utf-8") as f:
    f.write('"project","commits_found","issue_history_found"\n')
    for r in rows:
        base = FOLDER[r["MS/NonMS"]]
        name = r["full_name"]
        commits = os.path.isfile(os.path.join(base, "commits", name + ".csv"))
        history = os.path.isfile(os.path.join(base, "issue_history", name + ".csv"))
        f.write(f'"{name}",{str(commits).upper()},{str(history).upper()}\n')
        print(f"{name}: commits={commits} issue_history={history}")
print(f"> wrote {out_path}")
