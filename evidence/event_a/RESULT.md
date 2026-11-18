# Event A: Result

Prediction (committed before execution, b5113ce8, 2026-10-28): `evidence/event_a/PREDICTION.md`
Status on 2026-11-18: **not run, still blocked.**

## Outcome

Event A was **not run**. The frozen test needs issue opening and closing dates for all 12 projects, and only 5 of 12
issue histories exist. Following the Week 9 decision (*"Keep the same 12 projects and the same test. Find and check the
missing data before running Event A."*, `docs/RQS_AND_DECISION.md`), we did not run the test on a partial sample.

**The prediction is neither supported nor refuted.** There are no Event A numbers.

## Why it stays blocked

| Reason | Evidence |
|---|---|
| Only 5/12 issue histories exist; commit files exist for 12/12. The re-check on 2026-11-18 gives exactly the same result as on 2026-10-30. | `event_a_file_check_20261030_083437.csv`, `event_a_file_check_20261118_135240.csv` (script: `file_check.py`) |
| The `Data/*/issues/` files cover all 12 projects but have no `closed_at` column, so time-to-close cannot be computed from them. | Header of e.g. `Data/cases/issues/nymtech#nym.csv`: `number,created_at,user_login,user_id` |
| Week 9 first choice failed: the original data package has no issue histories for the 7 projects. `Data/projects.zip` (53,846 entries) and `Data/analyzedDataset.zip` (2,123 entries) contain no `issue_history` entries and no entries for any of the 7. | `data_package_check_20261118.txt` (script: `data_package_check.py`) |
| The 7 histories are also missing from our downloaded copy of the authors' package (Zenodo record 14876472, local copy dated 2026-10-12), and the online file list of that record (v1.0, 201,949 entries) has no issue history for any of the 7. It does list the histories of our other 5 projects. | `package_comparison_20261118.txt` |
| Week 9 fallback (collect from the GitHub Issues API) is not possible with the original method: `codes/main.py` imports `issueCrawler` from `codes/utils.py`, but `codes/utils.py` is missing from our downloaded copy of the authors' package (Zenodo record 14876472), is not in the online file list of that record either, and is not in any commit of this repository's history. Writing a new collector would be an unplanned change of method whose filtering rules (e.g. whether pull requests are excluded) cannot be checked against the original. | `codes/main.py` lines 4 and 223–225; `git log --all -- '*utils.py'` returns nothing; `package_comparison_20261118.txt` |

Missing issue histories, all for the reasons above:

| Project | Group | Issue history |
|---|---|---|
| nymtech#nym | MS | missing |
| SrinivasanTarget#ContractTestingBoilerplate | MS | missing |
| topcoder-platform#tc-project-service | MS | missing |
| ZeroCater#zc_events | MS | missing |
| rero#rero-mef | ~MS | missing |
| shlinkio#shlink | ~MS | missing |
| cofacts#rumors-api | ~MS | missing |

Four of the six MS projects are affected, so a run on the remaining 5 projects (2 MS, 3 ~MS) could not be compared with M2.

## Deviations from the plan

- Event A was not executed (planned: months 33–36, same 12 projects, frozen test).
- The Week 9 fallback (re-collect from the GitHub API) was not carried out, because the original collection script (`codes/utils.py`) is missing from our downloaded copy of the authors' package (Zenodo record 14876472) and from the online file list of that record.

## Effect on our conclusions

- The M2 result (W = 10, p = 0.1201, one-sided) stands for months 21–24 only; its stability over time is untested.
- RQ2 (sensitivity to project/time-window matching) is not answered.
- The Week 9 decision is unchanged: we do not have enough evidence to recommend a software design change.

## How to reproduce this check

```
python evidence/event_a/file_check.py
python evidence/event_a/data_package_check.py
```
Both use the Python standard library only and write new dated output files next to the old ones.
