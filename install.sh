#!/usr/bin/env bash
# LinkedIn Design Skills — installer
# Copies the `infographic` and `linkedin-carousel` Claude Code skills into ~/.claude/skills/
# Usage:  curl -sL https://raw.githubusercontent.com/victor-shulga/linkedin-design-skills/main/install.sh | bash
set -euo pipefail

REPO_URL="https://github.com/victor-shulga/linkedin-design-skills.git"
DEST="${HOME}/.claude/skills"
SKILLS=(infographic linkedin-carousel)

echo "→ Installing LinkedIn Design Skills into ${DEST}"

# Work from a local checkout if the script is run from inside the repo, else clone to a temp dir.
if [ -d "$(dirname "$0")/skills/infographic" ]; then
  SRC="$(cd "$(dirname "$0")/skills" && pwd)"
  CLEANUP=""
else
  command -v git >/dev/null 2>&1 || { echo "✗ git is required"; exit 1; }
  TMP="$(mktemp -d)"
  git clone --depth 1 "$REPO_URL" "$TMP" >/dev/null 2>&1
  SRC="${TMP}/skills"
  CLEANUP="$TMP"
fi

mkdir -p "$DEST"
for s in "${SKILLS[@]}"; do
  if [ -d "${DEST}/${s}" ]; then
    echo "  • ${s} already exists — backing up to ${s}.bak"
    rm -rf "${DEST}/${s}.bak"; mv "${DEST}/${s}" "${DEST}/${s}.bak"
  fi
  cp -R "${SRC}/${s}" "${DEST}/${s}"
  echo "  ✓ ${s}"
done

[ -n "${CLEANUP}" ] && rm -rf "${CLEANUP}"

cat <<'EOF'

✓ Done. Restart Claude Code, then run  /infographic  or  /linkedin-carousel

⚠ These ship with PLACEHOLDER brand (coral disc avatar, "YOUR LOGO").
  Rebrand before publishing anything — see README → "Rebrand in 5 minutes".
  Also: connect the Figma MCP first (see README → Prerequisites).
EOF
