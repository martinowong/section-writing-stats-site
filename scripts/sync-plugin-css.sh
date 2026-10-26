#!/bin/sh
# Copy styles.css from the plugin's latest release, so the site's badges,
# chips, and progress bars always match the released plugin.
set -eu
cd "$(dirname "$0")/.."
repo="martinowong/obsidian-section-meter"
version=$(curl -fsSL "https://api.github.com/repos/$repo/releases/latest" | sed -n 's/.*"tag_name": *"\([^"]*\)".*/\1/p')
[ -n "$version" ] || { echo "Could not find the latest release." >&2; exit 1; }
curl -fsSL "https://github.com/$repo/releases/download/$version/styles.css" -o plugin.css
sed -i.bak "s/plugin\.css?v=[^\"]*/plugin.css?v=$version/" index.html && rm index.html.bak
echo "plugin.css updated to $version"
