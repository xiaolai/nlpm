#!/usr/bin/env python3
"""Synthesize a findings sidecar from a legacy audit .md report.

Pre-v0.7.7 audits didn't emit `<slug>.findings.jsonl` — the sidecar
scheme shipped later, and the post-merge re-audit depends on that file
as its "before" snapshot. This tool parses the structured tables (and
subsection format) of a legacy audit report and emits a sidecar in the
shape `auditor/SCHEMAS.md §findings.jsonl` requires.

This is a LOSSY reconstruction. The live audit prompt asks Claude to
generate the sidecar directly from source files with richer context; we
can only recover what the markdown report committed to paper. In
particular:

  - `line` is usually `null` because most tables don't have a line
    column. When the issue text mentions "line N" we recover it.
  - `pattern` is slugified from the first few significant keywords of
    the issue text. It's not the exact pattern Claude would have used
    at audit time, but it's DETERMINISTIC: same input markdown always
    produces the same pattern, so fingerprints remain stable.
  - `rule_id` is inferred via a keyword table + fallback to `BUG-*` or
    `UNCLASSIFIED`. Rows that clearly match a vague-quantifier or
    missing-examples finding land on `R01` / `R09`.

Determinism is the hard contract. If a consumer re-runs the synthesizer
later, it MUST produce byte-identical sidecar output for the same .md —
otherwise fingerprints drift and the re-audit's diff is meaningless.

Usage:
    synthesize-sidecar.py auditor/audits/<slug>.md
    synthesize-sidecar.py --all auditor/audits/
    synthesize-sidecar.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Rule-ID and pattern inference. Order matters — first match wins, so more
# specific patterns must come before more general ones. Keys are regex
# fragments matched case-insensitively against the issue text.
# ---------------------------------------------------------------------------

# (pattern_regex, rule_id, pattern_slug) — first match wins.
# The pattern_slug is deterministic output; a match on ANY pattern_regex
# produces that slug regardless of which specific regex variant matched.
RULE_INFERENCE: list[tuple[str, str, str]] = [
    # Vague-quantifier — R01
    (r"vague\s*quantifier", "R01", "vague-quantifiers"),

    # Read-only + Write/Edit is MORE SPECIFIC than "no examples"; when
    # both appear in the same issue text (common in composite summary
    # rows), the structural bug wins. Keep these rules BEFORE the
    # example-block rules.
    (r"write/?edit\s+on\s+read[-\s]?only", "BUG-read-only-write", "write-edit-on-readonly"),
    (r"read[-\s]?only[^\n]*?\b(?:write|edit|allowed[-_]?tools)\b",
     "BUG-read-only-write", "write-edit-on-readonly"),
    (r"(?:do\s+not|don'?t)\s+(?:write|modify|edit)[^\n]*?\ballowed[-_]?tools\b",
     "BUG-read-only-write", "write-edit-on-readonly"),

    # Example blocks — R09. Patterns allow intermediate adjectives
    # ("zero usage examples", "no concrete examples", etc.) rather
    # than requiring "zero" and "example" to be adjacent tokens.
    (r"\bzero\s+(?:\w+\s+){0,3}examples?\b", "R09", "no-examples"),
    (r"\bno\s+(?:\w+\s+){0,3}examples?\b", "R09", "no-examples"),
    (r"no\s+`?<example>`?", "R09", "no-examples"),
    (r"missing\s+example", "R09", "no-examples"),

    # Frontmatter bugs — BUG-missing-frontmatter
    (r"no\s+yaml\s+frontmatter", "BUG-missing-frontmatter", "no-yaml-frontmatter"),
    (r"zero\s+yaml\s+frontmatter", "BUG-missing-frontmatter", "no-yaml-frontmatter"),
    (r"missing\s+`?name`?\s+field", "BUG-missing-frontmatter", "missing-name"),
    (r"missing\s+`?description`?\s+(?:frontmatter|field)",
     "BUG-missing-frontmatter", "missing-description"),
    (r"missing\s+`?date_added`?\s+field",
     "BUG-missing-frontmatter", "missing-date-added"),
    (r"no\s+`?name`?\b|missing\s+name\b",
     "BUG-missing-frontmatter", "missing-name"),
    (r"frontmatter\s+fragment|extra\s+`?---`?\s+separator",
     "BUG-invalid-frontmatter", "malformed-frontmatter"),

    # Allowed-tools — BUG-undeclared-tool
    (r"missing\s+`?allowed[-_]tools`?", "BUG-undeclared-tool", "missing-allowed-tools"),
    (r"no\s+`?allowed[-_]tools`?", "BUG-undeclared-tool", "missing-allowed-tools"),
    (r"missing\s+`?tools`?\s+(?:declaration|field)",
     "BUG-undeclared-tool", "missing-tools-declaration"),

    # Model tier
    (r"no\s+model\s+specified|missing\s+`?model`?\s+field",
     "BUG-missing-model", "missing-model"),

    # Unused tools
    (r"unused\s+tools?|tool.*not\s+used", "BUG-unused-tool", "unused-tools"),

    # Broken references
    (r"hardcoded\s+path", "BUG-broken-reference", "hardcoded-path"),
    (r"broken\s+reference|stale\s+reference", "BUG-broken-reference", "broken-reference"),
    (r"references?\s+wrong\s+(?:installation\s+)?domain",
     "BUG-broken-reference", "wrong-reference"),

    # Duplication / cross-component
    (r"identical\s+copy|full\s+duplication|duplicate", "CC-duplication", "duplicate-file"),
    (r"name\s+collision|names?\s+collide", "CC-name-collision", "name-collision"),

    # Malformed markdown
    (r"unclosed\s+code\s+fence|malformed\s+markdown", "BUG-malformed-markdown", "malformed-markdown"),

    # Version drift
    (r"version\s+drift", "CC-version-drift", "version-drift"),

    # Step ordering
    (r"skips?\s+step|step\s+ordering|no\s+numbered\s+(?:sequential\s+)?steps",
     "BUG-missing-steps", "missing-step-ordering"),

    # Ephemeral / task state in CLAUDE.md
    (r"ephemeral\s+(?:task\s+state|implementation[-\s]plan)",
     "BUG-ephemeral-context", "ephemeral-claude-md"),

    # Instruction override
    (r"instruction[-\s]override", "BUG-instruction-override", "instruction-override"),

    # Security — SEC-*
    (r"curl[-\s]pipe[-\s]sh|curl.*\|.*sh", "SEC-curl-pipe-sh", "curl-pipe-sh"),
    (r"eval\s+with\s+(?:variable|dynamic)", "SEC-eval-dynamic", "eval-dynamic"),
    (r"shell\s*=\s*true", "SEC-shell-true", "shell-true"),
    (r"postinstall\s+script", "SEC-postinstall-script", "postinstall-script"),
    (r"telemetry\s+webhook", "SEC-telemetry-exfil", "telemetry-exfil"),
    (r"credential\s+(?:exfil|extraction)", "SEC-credential-exfil", "credential-exfil"),
]

FALLBACK_SECURITY_RULE = "SEC-unknown"
FALLBACK_BUG_RULE = "BUG-unclassified"
FALLBACK_QUALITY_RULE = "UNCLASSIFIED"
FALLBACK_CROSSCOMP_RULE = "CC-unclassified"


def infer_rule_and_pattern(
    issue_text: str,
    category: str,
) -> tuple[str, str]:
    """Match issue_text against the RULE_INFERENCE table; return
    (rule_id, pattern_slug). When nothing matches, derive a pattern
    slug from the first few words and pick a namespaced fallback
    rule_id for the category."""
    text = issue_text.lower()
    for regex, rule_id, pattern in RULE_INFERENCE:
        if re.search(regex, text, re.IGNORECASE):
            return rule_id, pattern

    # Fallback pattern slug from the first 40 chars, keeping only
    # lowercase alphanumeric + hyphens. Deterministic — same input
    # text always produces the same slug.
    slug_src = re.sub(r"[`*_]", "", issue_text.lower())
    slug_src = re.sub(r"[^a-z0-9]+", "-", slug_src).strip("-")
    slug = slug_src[:40].rstrip("-") or "unspecified"

    fallback = {
        "security": FALLBACK_SECURITY_RULE,
        "bug": FALLBACK_BUG_RULE,
        "nl_quality": FALLBACK_QUALITY_RULE,
        "cross_component": FALLBACK_CROSSCOMP_RULE,
    }.get(category, "UNCLASSIFIED")
    return fallback, slug


# ---------------------------------------------------------------------------
# Section extraction
# ---------------------------------------------------------------------------

# Maps section title patterns (matched against lowercased header text)
# to a finding category. Legacy reports have varied titles; all variants
# of "Bugs (PR-worthy)", "Bugs", "Bugs (Must Fix)" land on "bug".
SECTION_CATEGORIES: list[tuple[str, str]] = [
    (r"^security\s+findings?\b", "security"),
    (r"^security\s+fixes?\b", "security"),
    (r"^bugs?\b", "bug"),
    (r"^quality\s+issues?\b", "nl_quality"),
    (r"^cross[-\s]?component", "cross_component"),
]


def classify_section_header(header: str) -> str | None:
    """Return the category this section contains, or None if this
    section isn't a findings section we care about."""
    # Strip leading ## hashes, then strip parenthetical qualifiers
    text = re.sub(r"^#+\s*", "", header).strip()
    text = re.sub(r"\s*\(.*?\)\s*$", "", text).strip().lower()
    for regex, category in SECTION_CATEGORIES:
        if re.search(regex, text):
            return category
    return None


def split_into_sections(md: str) -> list[tuple[str, str]]:
    """Split the markdown into (section_header, section_body) pairs.
    Splits on `## ` headers only; subsection `### ` headers stay inside
    their parent body."""
    lines = md.split("\n")
    sections: list[tuple[str, str]] = []
    current_header = ""
    current_body: list[str] = []
    for line in lines:
        if re.match(r"^##\s+\S", line) and not line.startswith("### "):
            if current_header or current_body:
                sections.append((current_header, "\n".join(current_body)))
            current_header = line
            current_body = []
        else:
            current_body.append(line)
    if current_header or current_body:
        sections.append((current_header, "\n".join(current_body)))
    return sections


# ---------------------------------------------------------------------------
# Table parsing
# ---------------------------------------------------------------------------

TABLE_HEADER_RE = re.compile(r"^\s*\|(.+)\|\s*$")
TABLE_SEP_RE = re.compile(r"^\s*\|[-:\s|]+\|\s*$")


def extract_tables(body: str) -> list[tuple[list[str], list[list[str]]]]:
    """Find pipe-table(s) in body. Returns list of (headers, rows).
    Each row is a list of cell strings aligned to the header list."""
    lines = body.split("\n")
    tables: list[tuple[list[str], list[list[str]]]] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = TABLE_HEADER_RE.match(line)
        if not m:
            i += 1
            continue
        # Next line must be the separator to confirm this is a table.
        if i + 1 >= len(lines) or not TABLE_SEP_RE.match(lines[i + 1]):
            i += 1
            continue
        headers = [c.strip() for c in m.group(1).split("|")]
        rows: list[list[str]] = []
        j = i + 2
        while j < len(lines):
            row_m = TABLE_HEADER_RE.match(lines[j])
            if not row_m:
                break
            cells = [c.strip() for c in row_m.group(1).split("|")]
            # Skip empty row
            if all(c == "" for c in cells):
                j += 1
                continue
            rows.append(cells)
            j += 1
        tables.append((headers, rows))
        i = j
    return tables


# Columns we recognise, mapped to canonical role names. Lowercased
# header text is matched substring-style — "File(s)" and "Files" and
# "Artifact" all resolve to "file".
COLUMN_ROLES: list[tuple[str, str]] = [
    (r"^#$|^no\b|^number$", "index"),
    (r"\bfiles?\b|\bartifacts?\b", "file"),
    (r"\btypes?\b", "type"),
    (r"\bscores?\b", "score"),
    (r"\bissues?\b|\bdescription\b|\btop\s+issue\b|\btop\s+penalty\b",
     "issue"),
    (r"\bimpact\b", "impact"),
    (r"\bpenalt(?:y|ies)\b", "penalty"),
    (r"\bseverit(?:y|ies)\b", "severity"),
    (r"\bfix\b|\brecommendation\b|\bsuggested[-\s]fix\b", "fix"),
    (r"\bline\b", "line"),
    (r"\bpatterns?\b", "pattern"),
]


def map_columns(headers: list[str]) -> dict[str, int]:
    """Return {role: column_index} for the roles this table exposes."""
    roles: dict[str, int] = {}
    for idx, header in enumerate(headers):
        h = header.lower().strip()
        for regex, role in COLUMN_ROLES:
            if re.search(regex, h):
                # First match wins per column; some headers like
                # "File | Type | Score | Top Issue" have a role per
                # column, and later roles won't overwrite earlier.
                if role not in roles:
                    roles[role] = idx
                break
    return roles


def clean_file_cell(raw: str) -> list[str]:
    """Split a file cell into individual file paths.

    A cell can hold:
      - `path/to/file.md` (one path)
      - `a.md`, `b.md`, `c.md` (comma-separated)
      - `a.md` AND `b.md` (joined with AND)
      - "All files in `agents/droids/`" (descriptive — one row that
        represents multiple files; we keep it as a single synthetic
        path so the finding survives the diff)
      - "All 20 agents" / "Repo-wide" (aggregate — return the raw
        text as a pseudo-path; the fingerprint will be stable and
        the caller knows this isn't a real path)
    """
    # Strip backticks for path extraction, but preserve the raw form
    # when nothing looks like a path.
    paths_found = re.findall(r"`([^`]+)`", raw)
    if paths_found:
        return [p.strip() for p in paths_found]
    # No backticked paths — check for bare-path-looking tokens.
    bare = re.findall(r"[A-Za-z0-9._/-]+\.(?:md|json|sh|py|yml|yaml)\b", raw)
    if bare:
        return bare
    # Aggregate row like "All 20 agents" — keep as single descriptive path.
    return [raw.strip()]


LINE_RE = re.compile(r"\bline[s]?\s+(\d+)\b", re.IGNORECASE)


def extract_line(text: str) -> int | None:
    m = LINE_RE.search(text)
    return int(m.group(1)) if m else None


PENALTY_RE = re.compile(r"-\s*(\d+)")


def extract_penalty(text: str) -> int | None:
    """Penalty cells look like `-8`, `−15`, `-5 each`, `-15 (zero examples)`."""
    m = re.search(r"[-−]\s*(\d+)", text)
    return -int(m.group(1)) if m else None


SEVERITY_ALIASES = {
    "critical": "critical",
    "high": "high",
    "medium": "medium",
    "med": "medium",
    "low": "low",
    "info": "info",
    "informational": "info",
}


def extract_severity(text: str) -> str:
    text_l = text.lower()
    for alias, canonical in SEVERITY_ALIASES.items():
        if re.search(rf"\b{alias}\b", text_l):
            return canonical
    return "info"


# ---------------------------------------------------------------------------
# Subsection parsing (nyldn-style)
# ---------------------------------------------------------------------------

SUBSECTION_HEADER_RE = re.compile(
    r"^###\s+(?:BUG|QUALITY|FINDING|SEC)[-\s]\d+.*$", re.IGNORECASE
)
FILE_LINE_RE = re.compile(
    r"^\s*\*\*Files?:\*\*\s*(.+)$", re.IGNORECASE
)
ISSUE_LINE_RE = re.compile(
    r"^\s*\*\*Issue:\*\*\s*(.+)$", re.IGNORECASE
)
SEVERITY_LINE_RE = re.compile(
    r"^\s*\*\*Severity:\*\*\s*(.+)$", re.IGNORECASE
)


def parse_subsection_block(body: str, category: str) -> list[dict]:
    """Parse a section whose findings are expressed as `### FOO-NNN`
    subsections with `**File:**`, `**Issue:**`, `**Severity:**` lines
    underneath. Each subsection becomes N findings, one per file listed
    in its File(s) line."""
    lines = body.split("\n")
    findings: list[dict] = []

    # Walk subsections: each starts at a `### ...-NNN` header.
    i = 0
    while i < len(lines):
        if not SUBSECTION_HEADER_RE.match(lines[i]):
            i += 1
            continue
        header = lines[i].strip()
        # The header itself often encodes the issue summary:
        # `### BUG-001 — description here`. Take everything after the
        # em-dash as the default issue text.
        header_body = re.sub(
            r"^###\s+(?:BUG|QUALITY|FINDING|SEC)[-\s]\d+\s*[—–-]\s*",
            "", header, flags=re.IGNORECASE,
        ).strip()

        files_cell = ""
        issue_text = header_body
        severity = ""

        j = i + 1
        while j < len(lines) and not (
            SUBSECTION_HEADER_RE.match(lines[j])
            or lines[j].startswith("## ")
        ):
            if m := FILE_LINE_RE.match(lines[j]):
                files_cell = m.group(1).strip()
            elif m := ISSUE_LINE_RE.match(lines[j]):
                issue_text = m.group(1).strip()
            elif m := SEVERITY_LINE_RE.match(lines[j]):
                severity = m.group(1).strip()
            j += 1

        files = clean_file_cell(files_cell) if files_cell else [header_body]
        for f in files:
            rule_id, pattern = infer_rule_and_pattern(issue_text, category)
            sev = extract_severity(severity) if severity else "info"
            line_no = extract_line(issue_text)
            findings.append({
                "category": category,
                "rule_id": rule_id,
                "file": f,
                "line": line_no,
                "severity": sev,
                "penalty": None,
                "pattern": pattern,
                "description": _one_line(issue_text),
                "false_positive": False,
                "suggested_fix": "",
            })

        i = j
    return findings


# ---------------------------------------------------------------------------
# Finding construction from tables
# ---------------------------------------------------------------------------

def _one_line(text: str) -> str:
    """JSONL forbids newlines inside string values. Flatten any stray
    whitespace / newlines to a single space, trim, cap length so the
    sidecar file stays readable."""
    collapsed = re.sub(r"\s+", " ", text).strip()
    return collapsed[:500]


def parse_table_findings(
    headers: list[str],
    rows: list[list[str]],
    category: str,
) -> list[dict]:
    """Each row becomes zero or more findings (zero if the File cell
    is empty; multiple if it lists several files)."""
    roles = map_columns(headers)
    if "file" not in roles or "issue" not in roles:
        return []

    findings: list[dict] = []
    for row in rows:
        if len(row) < len(headers):
            row = row + [""] * (len(headers) - len(row))
        file_cell = row[roles["file"]]
        issue_cell = row[roles["issue"]]
        if not file_cell.strip() or not issue_cell.strip():
            continue

        files = clean_file_cell(file_cell)
        # Penalty / impact / severity cells inform but don't change
        # the category.
        severity_cell = row[roles["severity"]] if "severity" in roles else ""
        penalty_cell = row[roles["penalty"]] if "penalty" in roles else ""
        fix_cell = row[roles["fix"]] if "fix" in roles else ""
        line_cell = row[roles["line"]] if "line" in roles else ""

        severity = (
            extract_severity(severity_cell)
            if severity_cell
            else extract_severity(issue_cell)
        )
        penalty = extract_penalty(penalty_cell) if penalty_cell else None
        line_no = extract_line(line_cell) if line_cell else extract_line(issue_cell)

        for f in files:
            rule_id, pattern = infer_rule_and_pattern(issue_cell, category)
            findings.append({
                "category": category,
                "rule_id": rule_id,
                "file": f,
                "line": line_no,
                "severity": severity if severity else "info",
                # Penalty only meaningful for nl_quality rows per the
                # SCHEMAS.md §findings.jsonl contract.
                "penalty": penalty if category == "nl_quality" else None,
                "pattern": pattern,
                "description": _one_line(issue_cell),
                "false_positive": False,
                "suggested_fix": _one_line(fix_cell) if fix_cell else "",
            })
    return findings


# ---------------------------------------------------------------------------
# Top-level
# ---------------------------------------------------------------------------

def synthesize(md_path: Path) -> list[dict]:
    """Parse one audit .md and return the list of finding dicts.

    Deterministic: same input file → same output list, in the same
    source order the report presents them (tables in header order,
    rows in table order, files in cell order)."""
    md = md_path.read_text()
    findings: list[dict] = []
    for header, body in split_into_sections(md):
        category = classify_section_header(header)
        if category is None:
            continue

        # Try tables first. Most legacy reports use them.
        had_tables = False
        for tbl_headers, tbl_rows in extract_tables(body):
            # Only consider tables whose headers include File + Issue.
            roles = map_columns(tbl_headers)
            if "file" in roles and "issue" in roles:
                had_tables = True
                findings.extend(parse_table_findings(tbl_headers, tbl_rows, category))

        # Subsection format — only if tables yielded nothing for this
        # section. Prevents double-counting when both formats appear.
        if not had_tables and re.search(r"^###\s+", body, re.MULTILINE):
            findings.extend(parse_subsection_block(body, category))

    return findings


def write_sidecar(findings: list[dict], out_path: Path) -> None:
    """Emit one JSON object per line, no pretty-printing, trailing
    newline on each record. Matches the shape audit.yml would emit."""
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as fh:
        for f in findings:
            fh.write(json.dumps(f, separators=(",", ":"),
                                ensure_ascii=False) + "\n")


# ---------------------------------------------------------------------------
# Self-tests
# ---------------------------------------------------------------------------

def _run_self_tests() -> int:
    fails = 0

    # Test 1: rule inference is stable and case-insensitive.
    for text, expected_rule, expected_pattern in [
        ('Vague quantifiers: "appropriate" x3', "R01", "vague-quantifiers"),
        ("No YAML frontmatter", "BUG-missing-frontmatter", "no-yaml-frontmatter"),
        ("Zero YAML frontmatter at all", "BUG-missing-frontmatter", "no-yaml-frontmatter"),
        ("Missing `allowed-tools`", "BUG-undeclared-tool", "missing-allowed-tools"),
        ("Hardcoded path `/Users/alice/...`", "BUG-broken-reference", "hardcoded-path"),
        ("Zero example interactions", "R09", "no-examples"),
        ("Zero usage examples across every agent", "R09", "no-examples"),
        ("No `<example>` blocks", "R09", "no-examples"),
        ("Identical copy of another agent", "CC-duplication", "duplicate-file"),
        # "read-only" + comma-separated Write/Edit tool names
        ('Body says "read-only research" but `allowedTools` includes `Write`, `Edit`',
         "BUG-read-only-write", "write-edit-on-readonly"),
        ("Read-only agent declares Write/Edit; no examples; NotebookEdit unused",
         "BUG-read-only-write", "write-edit-on-readonly"),
    ]:
        rule, pattern = infer_rule_and_pattern(text, "bug")
        if rule != expected_rule or pattern != expected_pattern:
            print(f"FAIL infer: input={text!r}\n"
                  f"  expected ({expected_rule}, {expected_pattern})\n"
                  f"  got      ({rule}, {pattern})", file=sys.stderr)
            fails += 1

    # Test 2: fallback slug is stable.
    for text, expect_prefix in [
        ("Some novel issue nobody has seen before", "some-novel-issue"),
        ("    edge case with whitespace    ", "edge-case-with-whitespace"),
    ]:
        rule, slug = infer_rule_and_pattern(text, "bug")
        if not slug.startswith(expect_prefix):
            print(f"FAIL fallback slug: input={text!r} got slug={slug!r}", file=sys.stderr)
            fails += 1
        if rule != FALLBACK_BUG_RULE:
            print(f"FAIL fallback rule: input={text!r} got rule={rule!r}", file=sys.stderr)
            fails += 1

    # Test 3: table parsing picks up File/Issue columns.
    sample_body = (
        "| # | File | Issue | Impact |\n"
        "|---|------|-------|--------|\n"
        "| 1 | `agents/foo.md` | No YAML frontmatter | Registration breaks |\n"
        "| 2 | `agents/bar.md` | Missing `description` field | Claude Code can't identify |\n"
    )
    tables = extract_tables(sample_body)
    assert len(tables) == 1, f"Expected 1 table, got {len(tables)}"
    findings = parse_table_findings(tables[0][0], tables[0][1], "bug")
    if len(findings) != 2:
        print(f"FAIL table parse: expected 2 findings, got {len(findings)}",
              file=sys.stderr)
        fails += 1
    elif findings[0]["file"] != "agents/foo.md":
        print(f"FAIL file extract: got {findings[0]['file']!r}", file=sys.stderr)
        fails += 1

    # Test 4: subsection parsing (nyldn shape).
    sample_sub = (
        "### BUG-001 — `.github/agents/` files have readonly conflict\n"
        "\n"
        "**Files:** `code-reviewer.md`, `performance-engineer.md`\n"
        "**Severity:** BUG — agents cannot execute.\n"
        "\n"
    )
    findings = parse_subsection_block(sample_sub, "bug")
    if len(findings) != 2:
        print(f"FAIL subsection parse: expected 2, got {len(findings)}",
              file=sys.stderr)
        fails += 1

    # Test 5: determinism — parsing same input twice yields byte-equal output.
    first = json.dumps(
        parse_table_findings(tables[0][0], tables[0][1], "bug"),
        sort_keys=True,
    )
    second = json.dumps(
        parse_table_findings(tables[0][0], tables[0][1], "bug"),
        sort_keys=True,
    )
    if first != second:
        print("FAIL determinism: same input produced different output",
              file=sys.stderr)
        fails += 1

    # Test 6: fingerprint stability — run the computed output through
    # compute-fingerprint.sh and confirm each row produces a valid
    # fingerprint with no crashes.
    import subprocess
    script_dir = Path(__file__).resolve().parent
    shell_helper = script_dir / "compute-fingerprint.sh"
    for f in findings:
        payload = json.dumps(f)
        cmd = (
            f'source "{shell_helper}" && '
            f'printf "%s" {json.dumps(payload)} | compute_fingerprint "demo/repo"'
        )
        result = subprocess.run(
            ["bash", "-c", cmd], capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.startswith("sha256:"):
            print(f"FAIL fingerprint: row={f} err={result.stderr}", file=sys.stderr)
            fails += 1

    if fails:
        print(f"\nsynthesize-sidecar.py self-tests: {fails} failure(s)",
              file=sys.stderr)
        return 1
    print("synthesize-sidecar.py self-tests: OK")
    return 0


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", type=Path,
                        help="Path to audit .md file, or directory when --all")
    parser.add_argument("--all", action="store_true",
                        help="Process every *.md in the given directory")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--output", type=Path, default=None,
                        help="Output sidecar path (single-file mode only)")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print synthesized findings to stdout instead of writing")
    args = parser.parse_args()

    if args.self_test:
        return _run_self_tests()

    if args.input is None:
        parser.error("input is required unless --self-test")

    if args.all:
        if not args.input.is_dir():
            parser.error(f"{args.input} is not a directory")
        total = 0
        for md_path in sorted(args.input.glob("*.md")):
            if md_path.name.endswith(".re-audit.md") or md_path.name.endswith(
                    ".re-audit.diff.md"
            ):
                continue
            findings = synthesize(md_path)
            sidecar_path = md_path.with_name(md_path.stem + ".findings.jsonl")
            if args.dry_run:
                print(f"--- {md_path.name} → {len(findings)} findings ---")
                for f in findings:
                    print(json.dumps(f, ensure_ascii=False))
            else:
                write_sidecar(findings, sidecar_path)
                print(f"{md_path.name}: {len(findings)} findings → {sidecar_path.name}")
            total += len(findings)
        print(f"\nTotal: {total} findings across {len(list(args.input.glob('*.md')))} files")
        return 0

    # Single-file mode
    findings = synthesize(args.input)
    if args.dry_run:
        for f in findings:
            print(json.dumps(f, ensure_ascii=False))
        return 0
    out = args.output or args.input.with_name(args.input.stem + ".findings.jsonl")
    write_sidecar(findings, out)
    print(f"{len(findings)} findings → {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
