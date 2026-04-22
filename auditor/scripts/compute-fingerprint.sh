#!/bin/bash
# Compute SCHEMAS §fingerprint for a finding record.
#
# The fingerprint is the join key between findings.jsonl, finding_outcome
# events, and disagreements.jsonl. Stability across workflows is a hard
# contract — drift here silently breaks every per-rule metric.
#
# Formula: sha256("<repo>|<file>|<rule_id>|<pattern>|<line>")
# - empty string for missing file/rule_id/pattern
# - literal "null" for missing line (includes null-value, not absent-key)
#
# Usage:
#   source auditor/scripts/compute-fingerprint.sh
#   FP=$(printf '%s' "$finding_json" | compute_fingerprint "<repo>")
#
# Callers:
#   - auditor-audit.yml aggregate step (enriches sidecar into findings.jsonl)
#   - auditor-contribute.yml sidecar prep (passes fingerprints to PR metadata)

compute_fingerprint() {
  local repo="$1"
  jq -r --arg repo "$repo" \
    '"\($repo)|\(.file // "")|\(.rule_id // "")|\(.pattern // "")|\(.line // "null")"' \
    | shasum -a 256 | awk '{print "sha256:" $1}'
}
