#!/usr/bin/env bash
# 사이트 파일을 main 과 gh-pages 두 브랜치에 올린다.
# (GitHub Pages 가 gh-pages 브랜치를 바라보고 있으므로 gh-pages 반영이 실제 배포다)
set -euo pipefail
cd "$(dirname "$0")"

REPO="https://github.com/seongkuy0427-blip/mail-board.git"
MSG="${1:-update: 대시보드 갱신}"

echo "== 1/2 main 브랜치"
git add -A
git commit -m "$MSG" || echo "  (변경 없음)"
git push origin main

echo "== 2/2 gh-pages 브랜치 (실제 배포)"
TMP="$(mktemp -d)"
cp -f index.html data.enc.json .nojekyll README.md "$TMP"/
(
  cd "$TMP"
  git init -q
  git config user.email "358577614+seongkuy0427-blip@users.noreply.github.com"
  git config user.name "seongkuy0427-blip"
  git add -A
  git commit -q -m "$MSG"
  git push -f "$REPO" HEAD:gh-pages
)
rm -rf "$TMP"

echo "== 완료: https://seongkuy0427-blip.github.io/mail-board/  (반영까지 30~60초)"
