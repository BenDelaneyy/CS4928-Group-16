#!/usr/bin/env bash
# Event B: measure change spread of the same cross-cutting feature (request/correlation ID in every
# request + log line) in one MS and one monolith project from our sample. Uses the real commits in
# which each project added the feature. Usage: bash evidence/event_b/change_spread.sh  (needs git + network)
set -euo pipefail
WORK=$(mktemp -d)
OUT="$(cd "$(dirname "$0")" && pwd)/change_spread.csv"
cd "$WORK"
git clone -q --filter=blob:none --no-checkout https://github.com/ministryofjustice/opg-use-an-lpa.git opg
git clone -q --filter=blob:none --no-checkout https://github.com/shlinkio/shlink.git shlink

echo "project,style,change,ref,date,file,component,kind,added,deleted" > "$OUT"
classify() { # $1 project $2 style $3 change $4 ref $5 date ; numstat on stdin
  while IFS=$'\t' read -r a d f; do
    case "$f" in service-api/*) comp=service-api;; service-front/*) comp=service-front;; service-pdf/*) comp=service-pdf;; *) comp=app;; esac
    case "$f" in
      CHANGELOG.md) kind=docs;;
      */docker/*|*Dockerfile*|*nginx*|*fpm-pool*) kind=infra;;
      *test*|*features/*|*behat*) kind=test;;
      *composer.json|*composer.lock|*/config/*|config/*) kind=config;;
      *) kind=src;;
    esac
    echo "$1,$2,$3,$4,$5,$f,$comp,$kind,$a,$d"
  done >> "$OUT"
}
# opg-use-an-lpa (MS): PR #211 (merge 7f1fbc53) + follow-up log processor commits b8fb8710, 7a2c7587
( cd opg
  git diff --numstat 7f1fbc53^1...7f1fbc53^2 | classify opg-use-an-lpa MS "initial: PR #211" 7f1fbc53 2020-02-13
  git show --numstat --format= b8fb8710 | grep . | classify opg-use-an-lpa MS "initial: log processor" b8fb8710 2020-02-18
  git show --numstat --format= 7a2c7587 | grep . | classify opg-use-an-lpa MS "initial: log processor" 7a2c7587 2020-02-18 )
# shlink (monolith): PR #662 (merge 86009543) + later fixes
( cd shlink
  git diff --numstat 86009543^1...86009543^2 | classify shlink ~MS "initial: PR #662" 86009543 2020-02-21
  git show --numstat --format= 4a1e7b8d | grep . | classify shlink ~MS "later fix: apply to non-REST routes" 4a1e7b8d 2021-12-19
  git show --numstat --format= 0f894dcd | grep . | classify shlink ~MS "later fix: replace abandoned dependency" 0f894dcd 2024-02-04 )
rm -rf "$WORK"
echo "> wrote $OUT"
