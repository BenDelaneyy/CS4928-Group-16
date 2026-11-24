<!--
Final synthesis draft, CS4928 Group 16, Project 22.
Text for an IEEE conference-format paper (max. 6 pages excluding references).
All evidence paths are relative to https://github.com/BenDelaneyy/CS4928-Group-16 at tag FINAL.
FINAL was moved on 2026-11-24 from cd3f416e (2026-11-18) to include evidence/confounders/, docs/AI_USE.md and the RQ history in docs/RQS_AND_DECISION.md.
-->

# Does Microservice Adoption Change Issue-Closing Velocity? A Bounded Reproduction with Two Change Events

**Authors:** CS4928 Group 16, Project 22: Kacper Banasik, Ben Delaney, Shakeeba Hamdam, Cathal Molloy, Killian Murnane

**Abstract** — We reproduce the crude end-velocity comparison of the EMSE study *"Does Microservice Adoption Impact the Velocity? A Cohort Study"* [1] on a sample of 12 projects. A one-sided Wilcoxon rank-sum (Mann-Whitney) test finds no significant difference in issue time-to-close between 6 microservice (MS) and 6 non-microservice (~MS) projects (W = 10, p = 0.1201), which matches the original non-significant result. A planned re-run in a later window (Event A) was not carried out because 7 of the 12 issue histories are missing. Neither those histories nor the script that downloaded them are in our copy of the authors' package (Zenodo record 14876472) or in the online file list of that record. For Event B we measured a cross-cutting feature request (a correlation ID on every request and log line) on the real commits of one matched PHP pair. It took 60 files and 2 deployables in the MS project and 7 files and 1 deployable in the monolith. We still do not have enough evidence to recommend a software design change, and the lack of a significant velocity difference is not evidence about maintainability.

**Index Terms** — microservices, velocity, reproduction, mining software repositories, change impact.

## I. Research Questions

The research questions are recorded in the group workbook (RQs and Milestones, row G16/P22) and copied to `docs/RQS_AND_DECISION.md`.

- **RQ1:** Can the reported lack/presence of a velocity difference be reproduced on a small cohort?
- **RQ2:** How sensitive is the result to project/time-window matching?

**RQ history.** A copy of the workbook from 2026-10-12 shows an earlier wording, with RQ1 about the study's full original sample and RQ2 about a new, more recent sample. We replaced it with the RQs recommended in the P22 pack when we adopted the pack's bounded small-cohort target, before entering the decision rule and expected result. `docs/RQS_AND_DECISION.md` (RQ history) records the earlier wording and the dates between which it changed.

**Decision rule (preregistered).** Compare issue-closing velocity (average days from issue creation to closure) between MS and monolithic projects with a Mann-Whitney test. A p-value of 0.05 or more means no statistically significant difference, which is what the original paper found (p = 0.7013 one-sided, 0.5987 two-sided). We expected to reproduce p ≥ 0.05.

## II. Method

**Sample.** `Data/sample.py` (seed 42) keeps the entries of `Data/final_data_file.csv` that have no missing values, a positive end velocity, and a main language with both MS and ~MS projects. It samples 6 MS projects and pairs each with one ~MS project in the same language, which gives `Data/final_data_file_sample.csv` (12 projects in Python, Rust, Java, JavaScript and PHP). *Deviation:* the P22 project pack says to take the first 12 eligible items in stable order. We drew ours at random (seed 42) and matched them by language with `Data/sample.py`. Recording this deviation changed no result.

**Metric.** Velocity is the mean time-to-close, in days, of issues closed in a 3-month window, computed by `get_velocity()` in `codes/get_velocity.py`. Lower is faster. The end window is months 21 to 24 after the first commit (`evidence/event_a/PREDICTION.md`).

**Test (frozen).** `evidence/bounded_run/bounded_tests.R` follows `codes/crude-analysis.R`. It adds 0.01 to end velocity and takes the absolute value, then runs Shapiro-Wilk, the Wilcoxon rank-sum test (two-sided, and one-sided with `alternative = "less"`, MS < ~MS), a Welch t-test, and a Welch t-test with Cohen's d on cube-root-transformed values. α = 0.05.

**Verification.** A second group member re-ran the one-sided test with an independent script (`codes/Shakeeba_verification.R`, output `evidence/Shakeeba_verification_output.txt`, review `evidence/bounded_run/Shakeeba_M2_sample_review.pdf`) in R 4.6.1.

**Change events.** We committed each event's prediction before running it: Event A in `evidence/event_a/PREDICTION.md` (commit `b5113ce8`, 2026-10-28) and Event B in `evidence/event_b/PREDICTION.md` (commit `41b467fb`, 2026-11-10 16:13). The README "Reproducibility" section lists the commands to reproduce each step.

## III. Results (bounded reproduction)

Source: `evidence/bounded_run/bounded_results_output.txt`.

| Test | Statistic | p |
|---|---|---|
| Wilcoxon rank-sum, one-sided (MS < ~MS) | W = 10 | **0.1201** |
| Wilcoxon rank-sum, two-sided | W = 10 | 0.2403 |
| Welch t-test, raw | t = −1.109, df = 8.88 | 0.2967 |
| Welch t-test, cube root | t = −1.342, df = 9.73 | 0.21 |

Median end velocity was 7.20 days for MS and 19.74 days for ~MS. The estimated location shift was −10.73 days (95.3% CI −∞ to 15.5, one-sided), and Cohen's d on the cube-transformed values was 0.77. MS end velocities were not normally distributed (Shapiro-Wilk p = 0.034), which supports using the rank-based test.

No test is significant at α = 0.05, which matches the original non-significant crude result (two-sided p = 0.5987, one-sided p = 0.7013, recorded in `codes/crude-analysis.R` lines 194 and 198). The answer to RQ1 is yes: under our decision rule (p ≥ 0.05), the lack of a velocity difference reproduces on our 12-project cohort. The independent re-run gave the same W = 10, p = 0.1201. As the verification review notes, a non-significant result does not show that the groups are equivalent.

**Confounder audit** (`evidence/confounders/confounder_audit.R`, output `confounder_audit_output.txt`). This check is exploratory, was added on 2026-11-24, and does not change the frozen test. The sample matches main language exactly by design (5 languages, the same in both groups). For the study's six other covariates we measured the imbalance between groups (standardised mean difference, SMD) and each covariate's association with end velocity (Spearman ρ, n = 12). Two covariates are both imbalanced and related to the outcome. MS projects have more commits (median 842 vs 415.5, SMD 0.66), and projects with more commits close issues faster (ρ = −0.48), so this could make MS look faster. MS projects also have fewer contributors on average (SMD −0.27, with equal medians of 7.5), and projects with more contributors close issues faster (ρ = −0.37), which pushes in the opposite direction. Size, issue count and creation year are also imbalanced (|SMD| 0.29 to 0.54) but less related to velocity (|ρ| < 0.3). None of the group differences is significant (all p > 0.68), though with 6 projects per group that tells us little. The crude comparison is therefore not adjusted for project activity, and we cannot tell which way any bias runs.

**RQ2: not answered.** Event A was meant to test sensitivity to the time window, and it is blocked (Section V). We used only one project matching, the same-language pairs from `Data/sample.py`, and did not test any alternative.

## IV. Design Decision

**Week 9 decision** (quoted in `evidence/event_b/PREDICTION.md`): *"Keep the same 12 projects and the same test. Find and check the missing data before running Event A. We do not yet have enough evidence to recommend a software design change."* The design problem and alternatives below come from the workbook and are copied to `docs/RQS_AND_DECISION.md`.

*Problem:* our analysis needs issue opening and closing dates for every project, and missing files stop us from checking the full sample. *Alternatives:* (1) check the original data package for the missing issue histories; (2) collect them from the GitHub Issues API; (3) use only the five complete projects. We rejected option 3 because it would change the planned sample and leave too few projects to compare with M2. *Choice:* check the original data package first, because that keeps the same 12 projects, and fall back on collecting the histories again, which takes longer. We made no structural change to the study design.

**Design alternatives for the Event B concern** (`evidence/event_b/RESULT.md`, "Responses considered"):

| Option | Description | Main trade-off |
|---|---|---|
| A. No structural change | Add the ID in each service or app through the existing middleware pipeline. | Simple, and services stay independently deployable. In MS it duplicates code, so any later tracing change means shotgun surgery. |
| B. Shared tracing package | Move the 4 duplicated classes into one versioned package. | One place to change, but the services must upgrade the shared dependency together, which moves them toward a distributed monolith. |
| C. Infrastructure | Log a load-balancer or nginx trace header at the proxy. | Little application code, but application log lines and downstream calls still need the ID, so it cannot replace A or B. |

**Chosen: Option A for both projects.** Four configuration files are enough in the monolith. In the MS project, B is not yet justified: only 2 PHP services share about 150 duplicated lines, and one team owns both in one repository. B becomes worthwhile if a third PHP service appears or the copies drift apart.

## V. Change Event A (later window)

**Plan.** Re-run the frozen test on the same 12 projects in months 33 to 36. The prediction was that p would stay above 0.05 and MS would keep the lower median. A p-value below 0.05, or a flip in direction, would challenge the M2 conclusion (`evidence/event_a/PREDICTION.md`).

**Status: not run, still blocked** (`evidence/event_a/RESULT.md`). The data check found commit files for 12 of 12 projects but issue-history files for only 5 (`evidence/event_a/event_a_file_check_20261030_083437.csv`), and a re-check on 2026-11-18 gave the same result (`evidence/event_a/event_a_file_check_20261118_135240.csv`). The missing projects are nymtech#nym, SrinivasanTarget#ContractTestingBoilerplate, topcoder-platform#tc-project-service and ZeroCater#zc_events (all MS), and rero#rero-mef, shlinkio#shlink and cofacts#rumors-api (~MS). The files in `Data/*/issues/` cover all 12 projects but have no `closed_at` column, so they cannot give time-to-close.

We followed the Week 9 plan. Our first choice, the original data package (`Data/projects.zip`, `Data/analyzedDataset.zip`), has no issue histories for any of the 7 projects (`evidence/event_a/data_package_check_20261118.txt`). The fallback was to collect them again from the GitHub Issues API, but the original method cannot do this: `codes/main.py` imports the collector `issueCrawler` from `codes/utils.py`, and that file is missing from our copy of the authors' package (Zenodo record 14876472, local copy dated 2026-10-12) and from the history of our repository. The online file list of the record (v1.0) has neither `codes/utils.py` nor issue histories for the 7 projects, although it lists the histories of our other 5 (`evidence/event_a/package_comparison_20261118.txt`). Writing a new collector would change the method without a plan, and we could not check its filtering rules against the original. As decided in Week 9, we did not run the test on the 5 remaining projects, only 2 of which are MS. Event A has no result, so the prediction is neither supported nor refuted.

## VI. Change Event B (cross-cutting feature)

**Request.** *"Every incoming HTTP request gets a correlation (request) ID. The ID is passed on to any downstream service call and appears in every log line produced while handling that request."* We applied it to one matched PHP pair, `ministryofjustice/opg-use-an-lpa` (MS) and `shlinkio/shlink` (~MS).

**Prediction** (`evidence/event_b/PREDICTION.md`). We expected the monolith change to stay local (one middleware, the logging config, 1 deployable, 1 or 2 tests). We expected the MS change to repeat in every service and inter-service client, touch several deployables and need a cross-service test. Each MS change would be small, and the extra cost would come from spread and coordination. We expected the Week 9 decision to be partly supported.

**Measurement.** Both projects had implemented this exact feature in February 2020, so `evidence/event_b/change_spread.sh` measures the real commits (opg PR #211 plus 2 log-processor commits; shlink PR #662) and writes one row per changed file to `evidence/event_b/change_spread.csv`.

| | opg-use-an-lpa (MS) | shlink (monolith) |
|---|---|---|
| Files changed | **60** | **7** |
| Lines added / deleted | +1638 / −345 | +47 / −13 |
| Deployables changed | 2 | 1 |
| Source / test / infra / config | 22 / 28 / 6 / 4 | 2 / 0 / 0 / 4 (+1 changelog) |
| Duplicated classes | 4, copied into both services | none |

The MS change touched about 9 times as many files and 35 times as many lines. Its individual classes are small (18 to 48 lines). The opg Node.js `service-pdf` still had no trace logging at month 24. shlink first covered REST routes only and fixed this in 2021 (`4a1e7b8d`); in 2024 it replaced its abandoned third-party library (`0f894dcd`).

**Prediction vs result.** All four predicted points held. The monolith change was smaller than we predicted, with no source changes and no tests. Neither of the conditions that would have challenged the prediction occurred.

**Response and accepted trade-off.** We chose Option A (Section IV). We accept duplicated tracing code in two MS services, with the shotgun-surgery risk that comes with it, to avoid a shared dependency that both services would have to version together. The Week 9 decision is partly supported: our method and sample need no change, but Event B shows a design cost that time-to-close velocity cannot measure.

## VII. AI-Assisted Engineering

We used AI tools to read code, plan the events, write analysis scripts and draft text, and `docs/AI_USE.md` lists the contributions that affected a decision. We did not use AI output as evidence; every number comes from a committed script or output. Checking the AI's work changed what we did three times. The assistant first worked from the wrong event card (P16 instead of P22) until we compared it with our repository. When our attempt to run the authors' `codes/main.py` failed, it traced the failure to a missing `codes/utils.py`, which later became part of the Event A evidence, and we used the R script instead. We also rejected its shared tracing package for Event B as over-engineering for two services. The Event B counts come from `change_spread.sh` run on public git history, and a group member confirmed the Event A data gap with a separate script.

## VIII. Limitations and Threats to Validity

- **Statistical power (most serious).** Each group has only 6 projects. A Cohen's d of 0.77 (cube-transformed) was still not significant, so the test is unlikely to detect even moderate differences, and a non-significant result is not evidence of equivalence. We did not run a power analysis on our sample.
- **Sample.** The 12 projects come from one seeded sample (`Data/sample.py`), and the verification review did not establish that they are representative. The sampling also departs from the P22 project pack, which asks for the first 12 eligible items in stable order. Another valid sample could give a different p-value, and we did not test this. The crude test is not adjusted for confounders, and the audit (Section III) found imbalance in commits and contributors, both of which relate to velocity.
- **Event A not run.** Our conclusion rests on a single time window. Stability over time is untested, and RQ2 stays open.
- **Missing collection script.** The script that downloaded the issue histories (`codes/utils.py`, imported by `codes/main.py`) is missing from our copy of the authors' package (Zenodo record 14876472) and from the online file list of that record. The missing histories cannot be collected again with the original method, and the existing ones cannot be regenerated or checked against their source.
- **Event B is n = 1 per style.** Different teams maintain the two projects: a government team with heavy acceptance testing, and a mostly single maintainer. Part of opg's test diff is refactoring, so its test-line count overstates the minimum effort. The scope also differs, because opg forwards an upstream ID while shlink has no downstream services.
- **Construct validity.** Issue time-to-close measures responsiveness. Event B shows that it does not capture change effort or maintainability.
- **Records.** The RQ wording changed in the workbook between 2026-10-12 and 2026-10-28, and the earlier wording was not kept visible there; `docs/RQS_AND_DECISION.md` now records it. The RQs and Week 9 alternatives live in the external workbook and were copied into the repository on 2026-11-18. No script generated the original Event A data check (2026-10-30), but the re-check on 2026-11-18 (`evidence/event_a/file_check.py`) reproduces it exactly. The tags `M2_REPRO`, `PRE_EVENT_A` and `PRE_EVENT_B` were added to the original commits on 2026-11-18, so the commit dates are the timing evidence. The Event B result was committed 7 minutes after its prediction. The bounded-run output did not record its R version; R 4.6.1 comes from the verification run.

## IX. Conclusion

On our 12-project sample the original finding reproduces: issue-closing velocity does not differ significantly between MS and ~MS projects (one-sided W = 10, p = 0.1201). We could not run the later-window check (Event A), because seven issue histories are missing and neither they nor the original download script are in the authors' package (Zenodo record 14876472, in both our copy and the online file list). Event B found that the same cross-cutting feature cost the MS project about 9 times as many files and 2 deployables instead of 1, so velocity alone cannot support a claim about maintainability. We do not have enough evidence to recommend a software design change. For the concern we observed, we keep the smallest response (no structural change) and accept duplicated tracing code. RQ2 (sensitivity to project/time-window matching) remains open, and the crude result is not adjusted for the project-activity confounders found in our audit. Future work is to obtain the original collection script or the 7 issue histories from the authors, run Event A as preregistered, and measure change spread on more than one pair.

## References

[1] N. Saarimäki, M. Robredo, V. Lenarduzzi, S. Vegas, N. Juristo, and D. Taibi, "Does microservice adoption impact the velocity? A cohort study," *Empirical Software Engineering*, vol. 30, no. 5, art. 130, 2025, doi: 10.1007/s10664-025-10673-7.

[2] CS4928 Group 16, replication repository, https://github.com/BenDelaneyy/CS4928-Group-16, tag FINAL.
