# Matchaism Portal

[![pages-build-deployment](https://github.com/matchaism/website/actions/workflows/pages/pages-build-deployment/badge.svg?branch=deploy)](https://github.com/matchaism/website/actions/workflows/pages/pages-build-deployment) [![get-atcoder-user-history-json](https://github.com/matchaism/website/actions/workflows/get-atcoder-user-history-json.yml/badge.svg?branch=deploy)](https://github.com/matchaism/website/actions/workflows/get-atcoder-user-history-json.yml)

[Matchaism Portal](https://portal.matchaism.net/)で公開

## Development

### `./*.html`

基本となるページはすべてここにある．英語版は`./eng/`直下にまとめている．

### `./(lifehack|work)/*.html`

制作物(lifehack|work)の詳細を紹介するページはここにある．`./work.html`からジャンプできる．

### `./component/`

- `./component/header.html`: 各種ページ上部のヘッダー
- `./component/(lifehack|work)/`: `./work.html`に掲載するworkやlifehackの中身はここ

## Deploy

- deployブランチでpushが発生すると，Actionsが実行
  - get-atcoder-user-history-jsonの実行 (build)
  - GitHub Pagesの更新 (build-deploy)
- 指定したタイミングでActionsが自動で実行
  - get-atcoder-user-history-json (JST 02:00 Monday)

### Procedure

 1. Develop
 2. Commit changes to local develop branches
 3. Merge into local master branch
 4. Push and update remote main branch
 5. Merge remote main branch into remote deploy branch
 6. Will run actions automatically to deploy
