# Event B — Prediction (recorded before execution)

Recorded: 2026-11-10, before any Event B repository was cloned or analysed.

## Frozen pre-Event-B state (Week 9 decision, unchanged)
"Keep the same 12 projects and the same test. Find and check the missing data before running Event A.
We do not yet have enough evidence to recommend a software design change."
Evidence: `evidence/event_a/event_a_file_check_20261030_083437.csv`

## The two architectural styles / snapshots
One matched pair from our 12-project sample, same language (PHP) so language does not skew the comparison:
- Microservices (MS): `ministryofjustice/opg-use-an-lpa`, snapshot = last commit before month 24 after first commit (2019-02-22 + 24 months = 2021-02-22)
- Monolith (~MS): `shlinkio/shlink`, snapshot = last commit before month 24 after first commit (2016-04-08 + 24 months = 2018-04-08)
Month 24 is the end of the paper's velocity window, i.e. the state the M2 result describes.

## Cross-cutting feature request (applied identically to both)
"Every incoming HTTP request gets a correlation (request) ID. The ID is passed on to any downstream
service call and appears in every log line produced while handling that request."

## Measures
- Locality: number of files / components that must change
- Coordination: number of separately deployable units (services, containers, repos) that must change and release together
- Testing burden: test files that must be added or changed; whether cross-service/integration tests are needed

## Prediction
- Monolith (shlink): high locality. One request-entry point (middleware) plus the logging config; one deployable;
  one or two test files. No cross-component coordination.
- Microservices (opg-use-an-lpa): lower locality. The same change repeats in every service that receives requests,
  plus every service-to-service HTTP client must forward the ID; several deployables change together;
  testing needs at least one cross-service check that the ID survives a hop.
- Each individual change in the MS project should be small; the extra cost is spread and coordination, not complexity.
- Week 9 decision expected to be **partly supported**: no change to our analysis method is needed, but the result shows
  a real design cost of microservices that the velocity metric does not capture.

## What would challenge this prediction
- The MS project already has a shared library / gateway that handles requests or logging centrally, so the change is
  as local as in the monolith; or
- the monolith's request handling or logging is scattered, so its change spreads as widely as the MS project's.
