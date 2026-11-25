#!/bin/bash
# テストページを公開する: 個人情報チェック → noindex 確認 → commit/push → 公開URLに反映されるまで待つ
# 使い方: scripts/publish.sh <project> "<変更の一言>"
#   例: scripts/publish.sh yama-gear "ギア詳細に関連投稿を追加"
# 終了コード: 0=公開確認済み / 1=チェックで止めた / 2=反映を確認できなかった
set -euo pipefail

PROJECT="${1:?使い方: scripts/publish.sh <project> \"<変更の一言>\"}"
MSG="${2:-update preview}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BASE="https://kohtaroinoue-maker.github.io/kohtaro-preview-hub"
cd "$ROOT"

[ -d "$PROJECT" ] || { echo "❌ $PROJECT フォルダがありません"; exit 1; }

git pull -q --rebase --autostash

# 1. 個人情報・鍵のチェック（公開リポなので1件でも出たら止める）
PI='浩太郎|井上|kohtaro|kawase|川瀬|@gmail|@yahoo|@icloud|sk-[a-zA-Z0-9_-]{10,}|AIza[0-9A-Za-z_-]{20,}|ghp_[0-9A-Za-z]{20,}'
# リポ名と公開ドメインは URL として既に公開済みなので除外してから判定する
HITS=$(grep -rnE "$PI" "$PROJECT" | sed -E 's/kohtaro-preview-hub|kohtaroinoue-maker\.github\.io//g' | grep -E "$PI" || true)
if [ -n "$HITS" ]; then
  echo "$HITS"; echo "❌ 個人情報・鍵らしき文字列があります。伏せてからやり直してください"; exit 1
fi

# 2. noindex の確認（HTML すべて）
MISSING=$(grep -rLE 'name="robots" content="noindex' --include='*.html' "$PROJECT" || true)
if [ -n "$MISSING" ]; then
  echo "❌ noindex が入っていない HTML があります:"; echo "$MISSING"; exit 1
fi
echo "✅ 個人情報チェック・noindex OK"

# 3. commit / push（このプロジェクトとハブ目次だけ）
git add -- "$PROJECT" index.html
if git diff --cached --quiet; then
  echo "ℹ️  変更なし（commit は作りません）"
else
  git commit -q -m "feat($PROJECT): $MSG

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"
  git push -q
  echo "✅ push: $(git log --oneline -1)"
fi

# 4. 公開URLに反映されるまで待つ（変更したHTMLの中身が一致するまで）
FILES=$(git show --name-only --pretty=format: HEAD -- "$PROJECT" | grep '\.html$' || true)
[ -n "$FILES" ] || FILES=$(find "$PROJECT" -name 'index.html' -maxdepth 2 | head -1)
for f in $FILES; do
  url="$BASE/${f%index.html}"
  want=$(shasum "$f" | cut -c1-12)
  ok=""
  for i in $(seq 1 16); do
    got=$(curl -s "$BASE/$f?t=$(date +%s)" | shasum | cut -c1-12)
    if [ "$got" = "$want" ]; then ok=1; break; fi
    sleep 15
  done
  if [ -n "$ok" ]; then echo "🌐 反映済み: $url"; else echo "⚠️  4分待っても反映を確認できません: $url"; exit 2; fi
done
