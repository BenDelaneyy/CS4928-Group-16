"""
Velocity recomputation check (CS4928 Group 16, P22). Added 2026-11-24.

The P22 bounded task is to reproduce the calculation of issue-closing velocity. M2 used the precomputed
velocity_mean_end / velocity_mean_start from Data/final_data_file_sample.csv. This script recomputes both
from the raw issue histories with the authors' own functions, for every sample project that has an
issue history (5 of 12; see evidence/event_a/RESULT.md for the 7 that are missing).

It follows velocityAnalysis() in codes/get_velocity.py step by step: same columns, same timezone handling,
open_time = closed_at - created_at, getWindowDates() for the windows (start months 9-12, end months 21-24
after the first commit) and get_velocity() for the mean. The conversion to days copies
timedelta_to_days_decimal() in codes/format_data_for_analysis.py (line 299): days + hours/24, rounded to
3 decimals, which drops minutes and seconds. That module is not imported because it pulls in unrelated
dependencies.

Run from the repository root (needs pandas, numpy, python-dateutil):
    python evidence/velocity_check/recompute_velocity.py
"""
import os
import sys
from datetime import datetime

import pandas as pd

sys.path.insert(0, "codes")
from get_velocity import get_velocity, getWindowDates, STATUS_COL, OPENED_COL, CLOSED_COL  # noqa: E402

SAMPLE = "Data/final_data_file_sample.csv"
OUT = "evidence/velocity_check/velocity_check_output.txt"


def to_days(td):
    # codes/format_data_for_analysis.py line 299
    return round(td.days + td.components.hours / 24, 3) if pd.notnull(td) else None


lines = []
def log(s=""):
    print(s)
    lines.append(s)

log(f"Velocity recomputation check - {datetime.now():%Y-%m-%d %H:%M:%S} - pandas {pd.__version__}")
log(f"Sample: {SAMPLE}")
log("")
header = f"{'project':45} {'grp':4} {'window':6} {'n_closed':>8} {'recomputed':>10} {'file':>8} {'match':>5} {'exact_mean_days':>15}"
log(header)

sample = pd.read_csv(SAMPLE)
checked = matched = 0
for _, row in sample.iterrows():
    name = row["full_name"]
    grp = "cases" if row["MS/NonMS"] == "MS" else "controls"
    issue_file = os.path.join("Data", grp, "issue_history", name + ".csv")
    if not os.path.exists(issue_file):
        log(f"{name:45} {row['MS/NonMS']:4} {'-':6} {'':>8} {'no issue history':>10}")
        continue
    # same preprocessing as velocityAnalysis()
    df = pd.read_csv(issue_file, usecols=[STATUS_COL, OPENED_COL, CLOSED_COL], parse_dates=[OPENED_COL, CLOSED_COL])
    df[OPENED_COL] = pd.to_datetime(df[OPENED_COL]).dt.tz_localize(None).dt.tz_localize("UTC")
    df[CLOSED_COL] = pd.to_datetime(df[CLOSED_COL]).dt.tz_localize(None).dt.tz_localize("UTC")
    df["open_time"] = df[CLOSED_COL] - df[OPENED_COL]
    s1, s2, e1, e2 = getWindowDates(os.path.join("Data", grp, "commits", name + ".csv"))
    for label, (a, b), col in (("start", (s1, s2), "velocity_mean_start"), ("end", (e1, e2), "velocity_mean_end")):
        mean, _, _, n_closed, _ = get_velocity(a, b, df)
        days = to_days(mean)
        exact = mean.total_seconds() / 86400 if pd.notnull(mean) else float("nan")
        ok = days is not None and abs(days - row[col]) < 0.0005
        checked += 1
        matched += ok
        log(f"{name:45} {row['MS/NonMS']:4} {label:6} {n_closed:>8} {days!s:>10} {row[col]:>8} {str(ok):>5} {exact:>15.3f}")

log("")
log(f"Matched {matched} of {checked} recomputed values exactly (to 3 decimals) for "
    f"{checked // 2} projects with issue histories; {len(sample) - checked // 2} projects have no issue history.")

with open(OUT, "w") as f:
    f.write("\n".join(lines) + "\n")
