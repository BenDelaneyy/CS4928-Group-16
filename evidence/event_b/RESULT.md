# Event B: Result

Prediction (committed before execution, 41b467fb, 2026-11-10 16:13): `evidence/event_b/PREDICTION.md`
Raw evidence: `evidence/event_b/change_spread.csv` (one row per changed file)
Reproduce: `bash evidence/event_b/change_spread.sh` (needs git and network access)

## What we did

Feature request applied to both styles: *"Every incoming request gets a correlation/request ID. The ID is
forwarded to downstream calls and appears in every log line."*

When we checked the month-24 snapshots, we found that **both projects actually implemented this exact feature,
within a week of each other in February 2020**. So instead of a hypothetical change estimate we measured the
real changes from git history:

| | opg-use-an-lpa (MS, PHP) | shlink (monolith, PHP) |
|---|---|---|
| Change | PR #211 (2020-02-13) + log-processor commits b8fb8710, 7a2c7587 (2020-02-18) | PR #662 (2020-02-21) |
| Snapshot used for "pre" state | 8cf35389 (2021-02-19, month 24): feature present in api + front, absent in service-pdf | d2a04259 (2018-04-07, month 24): feature absent |
| Files changed | **60** | **7** (4 feature-related config files, 2 incidental src clean-ups, changelog) |
| Lines added / deleted | **+1638 / −345** | **+47 / −13** |
| Deployable components changed | **2** (service-api, service-front) | **1** |
| Source files | 22 | 0 feature-related (handled by a library + config) |
| Test files | **28** (unit tests + reworked Behat acceptance contexts) | **0** |
| Infra files (Dockerfile, nginx, php-fpm) | 6 (3 per service) | 0 |
| Duplicated code | 4 near-identical classes copied into both services (RequestTracingMiddleware, RequestTracing, PhpDiModifiableContainer, RequestTracingLogProcessor: 0–4 differing lines each, namespaces only) | none |
| Coverage gap | service-pdf (Node.js) never got trace logging by month 24 | REST routes only at first; fixed for all routes in 4a1e7b8d (2021-12-19) |
| Later cost | none found in window | abandoned 3rd-party library `php-middleware/request-id` replaced with own code in 0f894dcd (2024-02-04, 5 files, first test added) |

## Prediction vs result

| Predicted | Result |
|---|---|
| Monolith: one middleware + logging config, one deployable, 1–2 tests | **Confirmed, and smaller than expected.** 4 config files, no source code, **no tests**. |
| MS: change repeated in every service + inter-service clients, several deployables | **Confirmed.** Repeated in both PHP services, outgoing API/PDF clients changed to forward the header, 2 deployables plus nginx/fpm config each. |
| MS testing needs a cross-service check | **Confirmed.** 28 test files, including shared acceptance-test contexts reworked so the trace ID works across the suite. |
| Individual MS changes small; cost is spread + coordination | **Confirmed.** Core classes are 18–48 lines each; the cost is the number of places (≈9× the files, ≈35× the lines). |

The "would challenge" conditions did not occur: opg had no shared tracing library (the code was copied per service),
and shlink's request handling was not scattered (one pipeline config).

## Responses considered (step 2)

| Option | What it is | Main trade-off |
|---|---|---|
| **A. No structural change** | Add the ID per service / per app with the existing middleware pipeline. (What both projects did.) | Simple, each service stays independently deployable. In MS it duplicates code, so any future tracing change becomes *shotgun surgery* across services. |
| **B. Shared tracing package** | Extract the 4 duplicated classes into one versioned package used by every PHP service. | One place to change, but adds a shared dependency that services must upgrade together: coupling, and a step towards a *distributed monolith*. |
| C. Push it to infrastructure | Rely on the load balancer / nginx header (opg already reads AWS `X-Amzn-Trace-Id`) and log it at the proxy. | Little app code, but app-level log lines and downstream calls still need the ID, so it cannot fully replace A or B. |

**Smallest justified response (step 3):** **Option A for both.** In the monolith it is clearly enough (4 config files).
In the MS project, a shared package (B) is not justified yet: only 2 PHP services share the duplicated code (~150 lines),
and both are owned by one team in one repository, so keeping two copies in sync is cheaper than versioning and releasing a
shared library. B becomes worth it if a third PHP service appears or the copies start to drift.

## Conclusion on the Week 9 decision

Week 9 decision: *"Keep the same 12 projects and the same test… We do not yet have enough evidence to recommend a software design change."*

**Partly supported.**
- *Supported:* nothing in Event B requires changing our analysis method or sample, and the smallest response in both
  projects needs no new structure or pattern.
- *Not fully supported:* Event B shows a real, measurable design cost that our velocity metric (issue time-to-close) cannot see.
  The same feature cost ~9× more files, 2 deployables, and 28 test files in the MS project. "No significant velocity difference"
  (M2) therefore does **not** mean "no maintainability difference". Future conclusions should say this explicitly.

**Trade-off / anti-pattern risk still remaining:** *duplicated code across services* in opg-use-an-lpa (4 copied classes) is a
shotgun-surgery risk for any future tracing change, and the Node.js service-pdf was left out, so the cross-cutting concern
is incompletely applied. In the monolith, the risk was a *third-party dependency* that was later abandoned and had to be
replaced (2024).

## Limitations
- One matched pair (n = 1 per style); different teams (government team with heavy acceptance tests vs a mostly single maintainer).
- Part of opg's test diff is refactoring of Behat contexts made necessary by the change, so test-line counts overstate the
  minimum testing effort; the file count and the need to touch shared test infrastructure are the more reliable signals.
- The scope is not identical: opg forwards an upstream load-balancer trace ID to downstream services; shlink generates an ID and has no downstream services. That difference is itself part of the MS cost.
