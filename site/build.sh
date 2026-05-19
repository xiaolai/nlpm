#!/usr/bin/env bash
# Build nlpm.com.
#
# 1. Re-generate the reference Markdown from canonical SKILL.md sources.
# 2. Sync auditor outputs (dashboard + per-repo HTMLs + assets + vendor +
#    legacy single-page docs/) into site/public/ as static passthrough.
# 3. Run `pnpm build` (VitePress).
# 4. Write CNAME into the build output so GitHub Pages knows the domain.
#
# Output: site/.vitepress/dist/
set -euo pipefail

cd "$(dirname "$0")"/..
ROOT=$(pwd)
SITE="$ROOT/site"
PUBLIC="$SITE/public"
SRC_REPORTS="$ROOT/auditor/reports"

echo "==> Regenerating reference Markdown"
python3 "$ROOT/bin/nlpm-build-reference-md" --out "$SITE/reference"

echo "==> Syncing case studies into site/case-studies/"
SRC_CASES="$ROOT/case-studies"
DEST_CASES="$SITE/case-studies"
rm -rf "$DEST_CASES"
mkdir -p "$DEST_CASES"
if [ -d "$SRC_CASES" ]; then
  # Copy articles + cover images. Skip nothing — case-studies/ holds only
  # publishable artifacts.
  cp -R "$SRC_CASES"/. "$DEST_CASES/"
  python3 "$ROOT/bin/nlpm-build-case-studies-index" --out "$DEST_CASES"
else
  echo "(no case-studies/ source — skipping)"
fi

echo "==> Syncing auditor outputs into site/public/"
rm -rf "$PUBLIC"
mkdir -p "$PUBLIC"
# Copy everything from auditor/reports/ except the markdown daily reports.
# Per-repo HTMLs land at /<slug>.html; dashboard at /dashboard.html;
# legacy framework guide at /docs/index.html; assets/ and vendor/ shared.
( cd "$SRC_REPORTS" && find . -maxdepth 1 -mindepth 1 \
    \( -name '*.html' -o -name '*.json' -o -type d \) \
    -not -name 'dashboard.html.bak' \
    -exec cp -R {} "$PUBLIC/" \; )

# CNAME so GitHub Pages binds the custom domain.
echo "nlpm.com" > "$PUBLIC/CNAME"

echo "==> Building VitePress"
cd "$SITE"
pnpm install --silent
pnpm build

# Surface the dist path so callers can deploy from it.
echo ""
echo "Built: $SITE/.vitepress/dist"
# `ls | head` trips pipefail on broken-pipe; show the count instead.
echo "dist entries: $(ls "$SITE/.vitepress/dist" | wc -l | tr -d ' ')"
