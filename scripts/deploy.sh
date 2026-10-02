#!/usr/bin/env bash
# 明史站一键部署：构建 + dist 推 gh-pages（Pages 托管分支）
# 用法： bash scripts/deploy.sh
set -euo pipefail
cd "$(dirname "$0")/../.."
REPO="git@github.com:Tliens/ming-history.git"
WORK=/tmp/ming-history-ghpages

echo "▶ 构建..."
npx astro build

echo "▶ 同步到 gh-pages..."
rm -rf "$WORK"
git clone -q --no-checkout "$REPO" "$WORK"
cd "$WORK"
git config user.email "deploy@local" && git config user.name "deploy"
# 绑 cname 等 GitHub 自动提交过 CNAME，先同步远端
git pull -q --rebase origin gh-pages 2>/dev/null || git checkout -q --orphan gh-pages
rm -rf ./*
cp -R /Users/tlien/Desktop/history/dist/. .
touch .nojekyll
git add -A
git commit -qm "deploy: rebuild $(date +%Y-%m-%d\ %H:%M)"
git push -q origin gh-pages
echo "✓ gh-pages 已推送，Pages 约 1 分钟生效（缓存 max-age=600，验证加 ?v=随机参数）"
