<!--
Final synthesis draft — CS4928 Group 16, Project 22.
Text for an IEEE conference-format paper (max. 6 pages excluding references).
All evidence paths are relative to https://github.com/BenDelaneyy/CS4928-Group-16 at tag FINAL.
-->

# Does Microservice Adoption Change Issue-Closing Velocity? A Bounded Reproduction with Two Change Events

**Authors:** CS4928 Group 16, Project 22: Kacper Banasik, Ben Delaney, Shakeeba Hamdam, Cathal Molloy, Killian Murnane

**Abstract** — We reproduce, on a 12-project sample, the crude end-velocity comparison of the EMSE study *"Does Microservice Adoption Impact the Velocity? A Cohort Study"* [1]. A one-sided Wilcoxon rank-sum (Mann-Whitney) test finds no significant difference in issue time-to-close between 6 microservice (MS) and 6 non-microservice (~MS) projects (W = 10, p = 0.1201), which matches the original non-significant result. A planned re-run in a later window (Event A) was not run: 7 of 12 issue histories are missing, and neither they nor the original download script are in our downloaded copy of the authors' package (Zenodo record 14876472) or in the online file list of that record. A cross-cutting feature request (Event B: a correlation ID on every request and log line), measured on the real commits of one matched PHP pair, needed 60 files and 2 deployables in the MS project versus 7 files and 1 deployable in the monolith. We keep our position: there is not enough evidence to recommend a software design change, but "no significant velocity difference" does not mean "no maintainability difference".

**Index Terms** — microservices, velocity, reproduction, mining software repositories, change impact.

## I. Research Questions

The research questions are recorded in the group workbook (RQs and Milestones, row G16/P22) and copied to `docs/RQS_AND_DECISION.md`.

- **RQ1:** Can the reported lack/presence of a velocity difference be reproduced on a small cohort?
- **RQ2:** How sensitive is the result to project/time-window matching?

**Decision rule (preregistered).** Compare issue-closing velocity (average days from issue creation to closure) between MS and monolithic projects with a Mann–Whitney test. p ≥ 0.05 means no statistically significant difference, as the original paper found (p = 0.7013 one-sided, 0.5987 two-sided). We expected to reproduce p ≥ 0.05.

## II. Method

**Sample.** `Data/sample.py` (seed 42) keeps entries of `Data/final_data_file.csv` with no missing values, positive end velocity, and a main language that has both MS and ~MS projects. It samples 6 MS projects and pairs each with one ~MS project of the same language, giving `Data/final_data_file_sample.csv` (12 projects; Python, Rust, Java, JavaScript, PHP). *Deviation:* the P22 project pack says to take the first 12 eligible items in stable order. Our sample was instead drawn at random (seed 42) and language-matched by `Data/sample.py`. No result was changed by recording this.

**Metric.** Velocity is the mean time-to-close (days) of issues closed in a 3-month window, from `get_velocity()` in `codes/get_velocity.py`; lower is faster. The end window is months 21–24 after the first commit (`evidence/event_a/PREDICTION.md`).

**Test (frozen).** `evidence/bounded_run/bounded_tests.R` follows `codes/crude-analysis.R`: add 0.01 to end velocity, take the absolute value, then run Shapiro-Wilk, the Wilcoxon rank-sum test (two-sided and one-sided `alternative = "less"`, MS < ~MS), a Welch t-test, and a Welch t-test with Cohen's d on cube-root-transformed values. α = 0.05.

**Verification.** A second group member re-ran the one-sided test with an independent script (`codes/Shakeeba_verification.R`, output `evidence/Shakeeba_verification_output.txt`, review `evidence/bounded_run/Shakeeba_M2_sample_review.pdf`), using R 4.6.1.

**Change events.** Each event had its prediction committed before execution: Event A in `evidence/event_a/PREDICTION.md` (commit `b5113ce8`, 2026-10-28) and Event B in `evidence/event_b/PREDICTION.md` (commit `41b467fb`, 2026-11-10 16:13). Reproduction commands are in the README "Reproducibility" section.

## III. Results (bounded reproduction)

Source: `evidence/bounded_run/bounded_results_output.txt`.

| Test | Statistic | p |
|---|---|---|
| Wilcoxon rank-sum, one-sided (MS < ~MS) | W = 10 | **0.1201** |
| Wilcoxon rank-sum, two-sided | W = 10 | 0.2403 |
| Welch t-test, raw | t = −1.109, df = 8.88 | 0.2967 |
| Welch t-test, cube root | t = −1.342, df = 9.73 | 0.21 |

Median end velocity was 7.20 days (MS) and 19.74 days (~MS). The location shift estimate was −10.73 days (95.3% CI −∞ to 15.5, one-sided). Cohen's d on the cube-transformed values was 0.77. MS end velocities were not normal (Shapiro-Wilk p = 0.034), which supports the rank-based test.

No test is significant at α = 0.05. This matches the original non-significant crude result (two-sided p = 0.5987, one-sided p = 0.7013, recorded in `codes/crude-analysis.R` lines 194 and 198). **RQ1: yes — under our decision rule (p ≥ 0.05) the lack of a velocity difference reproduces on our 12-project cohort.** The independent re-run gave the same W = 10, p = 0.1201. As the verification review notes, a non-significant result does not show that the groups are equivalent.

**RQ2: not answered.** Testing sensitivity to the time window was the purpose of Event A, which is blocked (Section V). We ran only one project matching: same-language pairs from `Data/sample.py`. No alternative matching was tested.

## IV. Design Decision

**Week 9 decision** (quoted in `evidence/event_b/PREDICTION.md`): *"Keep the same 12 projects and the same test. Find and check the missing data before running Event A. We do not yet have enough evidence to recommend a software design change."* The design problem and alternatives below are from the workbook, copied to `docs/RQS_AND_DECISION.md`.

*Problem:* our analysis needs issue opening and closing dates for every project, and missing files stop us from checking the full sample. *Alternatives:* (1) check the original data package for the missing issue histories; (2) collect them from the GitHub Issues API; (3) use only the five complete projects. Option 3 was rejected because it would change the planned sample and leave too few projects to compare with M2. *Choice:* check the original data package first, because it keeps the same 12 projects; collecting the histories again is the fallback, as it takes more time. No structural change to the study design was made.

**Design alternatives for the Event B concern** (`evidence/event_b/RESULT.md`, "Responses considered"):

| Option | Description | Main trade-off |
|---|---|---|
| **A. No structural change** | Add the ID per service/app through the existing middleware pipeline. | Simple, and services stay independently deployable. In MS it duplicates code, so future tracing changes become shotgun surgery. |
| B. Shared tracing package | Extract the 4 duplicated classes into one versioned package. | One place to change, but it adds a shared dependency that services must upgrade together (a step toward a distributed monolith). |
| C. Infrastructure | Log a load-balancer/nginx trace header at the proxy. | Little app code, but app log lines and downstream calls still need the ID, so it cannot replace A or B. |

**Chosen: Option A for both projects.** In the monolith, 4 configuration files are enough. In the MS project, B is not yet justified: only 2 PHP services share about 150 duplicated lines, and both are owned by one team in one repository. B becomes worthwhile if a third PHP service appears or the copies drift.

## V. Change Event A (later window)

**Plan.** Re-run the frozen test on the same 12 projects in months 33–36. Prediction: still p > 0.05, with MS keeping the lower median. The M2 conclusion would be challenged by p < 0.05 or by the direction flipping (`evidence/event_a/PREDICTION.md`).

**Status: not run, still blocked** (`evidence/event_a/RESULT.md`). The data check found commit files for 12/12 projects but issue-history files for only 5/12 (`evidence/event_a/event_a_file_check_20261030_083437.csv`); a re-check on 2026-11-18 gave the same result (`evidence/event_a/event_a_file_check_20261118_135240.csv`). The missing ones are nymtech#nym, SrinivasanTarget#ContractTestingBoilerplate, topcoder-platform#tc-project-service, ZeroCater#zc_events (all MS), rero#rero-mef, shlinkio#shlink and cofacts#rumors-api (~MS). The files in `Data/*/issues/` cover all 12 projects but have no `closed_at` column, so time-to-close cannot be computed from them.

We followed the Week 9 plan. First choice: the original data package (`Data/projects.zip`, `Data/analyzedDataset.zip`) contains no issue histories for any of the 7 projects (`evidence/event_a/data_package_check_20261118.txt`). Fallback: re-collect from the GitHub Issues API. This was not possible with the original method, because `codes/main.py` imports the collector `issueCrawler` from `codes/utils.py`. That file is missing from our downloaded copy of the authors' package (Zenodo record 14876472, local copy dated 2026-10-12) and from this repository's history. The online file list of the record (v1.0) contains neither `codes/utils.py` nor issue histories for the 7 projects, although it lists those of our other 5 (`evidence/event_a/package_comparison_20261118.txt`). A new collector would be an unplanned method change whose filtering rules cannot be checked against the original. As decided at Week 9, we did not run the test on the 5 remaining projects (only 2 of them MS). **There is no Event A result, and the prediction is neither supported nor refuted.**

## VI. Change Event B (cross-cutting feature)

**Request.** *"Every incoming HTTP request gets a correlation (request) ID. The ID is passed on to any downstream service call and appears in every log line produced while handling that request."* We applied it to one matched PHP pair: `ministryofjustice/opg-use-an-lpa` (MS) and `shlinkio/shlink` (~MS).

**Prediction** (`evidence/event_b/PREDICTION.md`). The monolith change would be local (one middleware, logging config, 1 deployable, 1–2 tests). The MS change would repeat in every service and inter-service client and touch several deployables, with a cross-service test. Each MS change would be small, with the extra cost coming from spread and coordination. The Week 9 decision would be partly supported.

**Measurement.** Both projects had implemented this exact feature in February 2020. `evidence/event_b/change_spread.sh` therefore measures the real commits (opg PR #211 plus 2 log-processor commits; shlink PR #662) and writes one row per file to `evidence/event_b/change_spread.csv`.

| | opg-use-an-lpa (MS) | shlink (monolith) |
|---|---|---|
| Files changed | **60** | **7** |
| Lines added / deleted | +1638 / −345 | +47 / −13 |
| Deployables changed | 2 | 1 |
| Source / test / infra / config | 22 / 28 / 6 / 4 | 2 / 0 / 0 / 4 (+1 changelog) |
| Duplicated classes | 4, copied into both services | none |

The ratios are about 9× the files and about 35× the lines. Individual MS classes are small (18–48 lines). The opg Node.js `service-pdf` had no trace logging by month 24. shlink first covered REST routes only, fixed this in 2021 (`4a1e7b8d`), and in 2024 replaced its abandoned third-party library (`0f894dcd`).

**Prediction vs result.** All four predicted points were confirmed, and the monolith change was smaller than predicted (no source changes and no tests). Neither "would challenge" condition occurred.

**Response and accepted trade-off.** We chose Option A (Section IV). We accept duplicated tracing code in two MS services, and the shotgun-surgery risk that comes with it, in exchange for avoiding a shared, co-versioned dependency. **Week 9 decision: partly supported.** No change to our method or sample is needed, but Event B shows a real design cost that time-to-close velocity cannot measure.

## VII. Limitations and Threats to Validity

- **Statistical power (most serious).** There are only 6 projects per group. Cohen's d of 0.77 (cube-transformed) was still non-significant, so the test is unlikely to detect even moderate differences. A non-significant result is not evidence of equivalence. We did not run a power analysis on our sample.
- **Sample.** The 12 projects come from one seeded sample (`Data/sample.py`). Representativeness was not established (verification review). The sampling also deviates from the P22 project pack, which asks for the first 12 eligible items in stable order. A different but equally valid sample could give a different p-value, which we did not test.
- **Event A not run.** Our conclusion rests on one time window, stability over time is untested, and RQ2 stays open.
- **Missing collection script.** The script that downloaded the issue histories (`codes/utils.py`, imported by `codes/main.py`) is missing from our downloaded copy of the authors' package (Zenodo record 14876472) and is not in the online file list of that record. The missing histories therefore cannot be re-collected with the original method, and the existing histories cannot be regenerated or checked against their source.
- **Event B is n = 1 per style.** The two projects have different teams (a government team with heavy acceptance tests versus a mostly single maintainer). Part of opg's test diff is refactoring, so test-line counts overstate the minimum effort. The scope also differs: opg forwards an upstream ID, while shlink has no downstream services.
- **Construct validity.** Issue time-to-close measures responsiveness, not change effort or maintainability (shown by Event B).
- **Records.** The RQs and Week 9 alternatives live in the external workbook and were copied into the repository on 2026-11-18. The original Event A data check (2026-10-30) has no generating script; the 2026-11-18 re-check (`evidence/event_a/file_check.py`) reproduces it exactly. Tags `M2_REPRO`, `PRE_EVENT_A` and `PRE_EVENT_B` were added on 2026-11-18 to the original commits, so commit dates are the timing evidence. The Event B result was committed 7 minutes after its prediction. The bounded-run output did not record its R version; R 4.6.1 comes from the verification run.

## VIII. Conclusion

On our 12-project sample, the original finding reproduces: there is no significant difference in issue-closing velocity between MS and ~MS projects (one-sided W = 10, p = 0.1201). The later-window check (Event A) was not run. Seven issue histories are missing, and neither they nor the original download script are in the authors' package (Zenodo record 14876472, both our downloaded copy and the online file list), so Event A has no result. Event B shows that the same cross-cutting feature cost the MS project about 9× the files and 2 deployables versus 1. Velocity alone therefore cannot support a claim about maintainability. **We do not have enough evidence to recommend a software design change.** For the observed concern we keep the smallest response (no structural change) and accept duplicated tracing code. RQ2 (sensitivity to project/time-window matching) remains open. Future work: obtain the original collection script or the 7 issue histories from the original authors and run Event A as preregistered, and measure change spread on more than one pair.

## References

[1] N. Saarimäki, M. Robredo, V. Lenarduzzi, S. Vegas, N. Juristo, and D. Taibi, "Does microservice adoption impact the velocity? A cohort study," *Empirical Software Engineering*, vol. 30, no. 5, art. 130, 2025, doi: 10.1007/s10664-025-10673-7.

[2] CS4928 Group 16, replication repository, https://github.com/BenDelaneyy/CS4928-Group-16, tag FINAL.
