#!/usr/bin/env bash
# pipeline/deploy_gh_pages.sh
# Deploys the locally compiled static dashboard (build/) directly to GitHub Pages (gh-pages branch)

set -e

BUILD_DIR="build"
BRANCH="gh-pages"
REMOTE="${1:-origin}"

echo "[Build] Compiling static SvelteKit cockpit..."
BASE_PATH="${BASE_PATH:-/nextstrain_dashboard}" npm run build

touch "$BUILD_DIR/.nojekyll"

echo "======================================================================"
echo "NextGen Surveillance: Local Static Deployment to GitHub Pages"
echo "======================================================================"
echo "Target Branch: $BRANCH"
echo "Target Remote: $REMOTE"

ROOT_DIR="$(pwd)"
TEMP_DIR=$(mktemp -d -t gh-pages-deploy-XXXXXX)

# Copy build contents into temporary git deployment repository
cp -r "$BUILD_DIR"/* "$TEMP_DIR"/
cp "$BUILD_DIR"/.nojekyll "$TEMP_DIR"/ 2>/dev/null || true

cd "$TEMP_DIR"
git init -b "$BRANCH"
git config user.name "Antigravity Deployer"
git config user.email "deploy@veg.org"
git add -A
git commit -m "deploy: live static surveillance cockpit update [$(date -u +'%Y-%m-%dT%H:%M:%SZ')]"

# Fetch remote URL from root repository
REMOTE_URL=$(git -C "$ROOT_DIR" config --get remote."$REMOTE".url || echo "")

if [ -n "$REMOTE_URL" ]; then
  echo "Pushing static pages to $REMOTE_URL ($BRANCH branch)..."
  if git push "$REMOTE_URL" "$BRANCH":"$BRANCH" --force; then
    echo ""
    echo "[✓] Successfully deployed static dashboard to GitHub Pages!"
    echo "    Host URL: https://veg.github.io/nextstrain_dashboard/"
    echo "    (or configured custom domain https://surveillance.veg.org/)"
  else
    echo ""
    echo "[!] Push to $REMOTE_URL failed (check remote repository access or SSH credentials)."
    echo "    The static build is ready in: $ROOT_DIR/$BUILD_DIR"
  fi
else
  echo "[Warning] No remote URL configured for '$REMOTE'."
fi

rm -rf "$TEMP_DIR"
cd "$ROOT_DIR"
echo "======================================================================"
