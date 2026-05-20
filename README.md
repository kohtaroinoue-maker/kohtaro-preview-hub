# kohtaro-preview-hub

各案件のテストページ・プレビューを置く汎用ハブリポ。Public + GitHub Pages 公開。

## 公開 URL

- ハブトップ: https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/
- 各案件: `https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/<project>/`

## 構造

```
.
├── index.html           ← 案件一覧（手動更新）
├── .nojekyll            ← Jekyll 無効化（_ で始まるファイルも配信）
├── robots.txt           ← Disallow: /
├── README.md
└── <project>/           ← 案件ごとのサブディレクトリ
    ├── index.html
    └── ...
```

## 現在の案件

| project | 内容 | URL |
|---|---|---|
| `golf-compe/` | 副業 06 ゴルフコンペアプリ — デザイン5パターン + Aurora 色違い | [/golf-compe/](https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/golf-compe/) |

## 公開ポリシー

- **noindex がデフォルト**: 全 HTML に `<meta name="robots" content="noindex,nofollow">`、ルート `robots.txt` で `Disallow: /`
- **PI 抽象化必須**: 実名・取引先・実在固有名詞・API キーは push 前にスキャン → 抽象化
- **demo データのみ**: 機密性なし
- **indexable 公開は明示指示が必要**: その時は別途方針確認

## 新案件の追加

本社リポ ([kohtaro-anything](https://github.com/kohtaroinoue-maker/kohtaro-anything)) のスキル `publish-test-page` を参照。
