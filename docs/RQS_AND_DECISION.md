# Copied from the group workbook (RQs and Milestones, row G16/P22) on 2026-11-18. Original record is the workbook.

RQ1: Can the reported lack/presence of a velocity difference be reproduced on a small cohort?

RQ2: How sensitive is the result to project/time-window matching?

Sample (12 projects): fedspendingtransparency#usaspending-api, nymtech#nym, SrinivasanTarget#ContractTestingBoilerplate, topcoder-platform#tc-project-service, ZeroCater#zc_events, ministryofjustice#opg-use-an-lpa, rero#rero-mef, openfun#richie, paritytech#substrate, hashgraph#hedera-mirror-node, shlinkio#shlink, cofacts#rumors-api

Method / decision rule: We will compare issue-closing velocity between the microservice and monolithic projects using a Mann–Whitney test. Issue-closing velocity is measured as the average number of days from issue creation to closure. A p-value ≥ 0.05 indicates no statistically significant difference between the groups, this is what the paper found.

Expected result: Expecting a reproduction on Mann-Whitney test p-value is ≥ 0.05 as with the paper, whose Mann-Whitney test p-values were 0.7013 (one-sided) and 0.5987 (two-sided).

Week 9 design problem: Our analysis needs issue opening and closing dates for every project. Missing files stop us from checking the full sample.

Week 9 alternatives considered: Possible options are to check the original data package (project.zip/Dataset.zip) for the missing issue histories, or to collect them from the GitHub Issues API. Using only five projects would change our planned sample and make the rest too weak to compare with M2. We chose to check the original data package first, because it keeps the same 12 projects, collecting the histories again is the fallback, as it takes more time.

Week 9 decision: Keep the same 12 projects and the same test. Find and check the missing data before running Event A. We do not yet have enough evidence to recommend a software design change.

## RQ history (added 2026-11-24)

The RQs above are not the first wording recorded for G16/P22. A copy of the shared workbook saved on 2026-10-12
(RQs and Milestones sheet, row G16/P22) shows the earlier wording:

- Earlier RQ1: *Can the reported difference in issue closing velocity be reproduced using the study's original sample of projects?*
- Earlier RQ2: *Does the same finding hold when applied to a new more recently created sample of projects?*

The current wording is the recommended wording in the P22 project pack. The change came with the move from the
study's full original sample (265 projects) to the pack's bounded target, "on a small matched cohort, reproduce the
calculation of issue-closing velocity", which our 12-project sample (`Data/sample.py`, M2, commit `49687d8b`,
2026-10-21) implements. The earlier RQ2 (a new, more recent sample) was replaced by the pack's RQ2 (sensitivity to
project/time-window matching), which Event A was planned to test. The change was made in the workbook between
2026-10-12 (earlier wording) and 2026-10-28 (current wording, Event A entry); the exact date was not recorded, and the
earlier wording should have been kept visible in the workbook at the time. In the 2026-10-12 copy only the two RQs
were filled in (sample, method, decision rule and expected result were still empty), so those fields were entered
once, with the current RQs.
