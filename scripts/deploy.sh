#!/usr/bin/env bash
# 明史站一键部署：构建 → gh-pages worktree 同步 → 推送（Pages 托管分支）
# 说明：与单文件站不同，本站 main 存源码、gh-pages 存 dist 产物；_astro/ 目录必须带 .nojekyll
set -euo pipefail
cd "$(dirname "$0")/.."
ROOT="$(pwd)"
WORK=/tmp/ming-history-ghpages

echo "▶ 构建..."
npx astro build

echo "▶ 同步 gh-pages worktree..."
git fetch -q origin gh-pages
git worktree remove --force "$WORK" 2>/dev/null || rm -rf "$WORK"
git worktree add -B gh-pages "$WORK" origin/gh-pages
# dist 覆盖，但保留 Pages 的 CNAME 与 .nojekyll
rsync -a --delete --exclude=".git" --exclude=".nojekyll" --exclude="CNAME" "$ROOT/dist/" "$WORK/"
touch "$WORK/.nojekyll"
cd "$WORK"
git add -A
if git diff --cached --quiet; then echo "✓ 无变化"; else
  git commit -qm "deploy: rebuild $(date +%Y-%m-%d\ %H:%M)"
  git push -q origin gh-pages
  echo "✓ gh-pages 已推送，Pages 约 1 分钟生效（验证加 ?v=随机参数 绕过 10 分钟缓存）"
fi
git worktree remove --force "$WORK"
