#!/bin/bash
# Publish Lox Café: rebuild the site, back it up to GitHub, deploy to Cloudflare.
# Live game: https://lox-cafe.pages.dev  (GitHub Pages copy keeps working too)
set -e
cd "$(dirname "$0")"
python3 build.py
export GH_CONFIG_DIR="$HOME/.gh-config" PATH="/usr/local/bin:$PATH"
git push -q || echo "GitHub push skipped (commit first, or check gh auth)"
"/Users/Franny/Claude Code/corkboard/node_modules/.bin/wrangler" pages deploy --branch main --commit-dirty=true
