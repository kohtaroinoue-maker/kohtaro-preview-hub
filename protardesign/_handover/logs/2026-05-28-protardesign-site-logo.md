# ProtarDesign 事業紹介サイト＆ロゴ 制作ログ

- 日付: 2026-05-28
- 担当: クロジロウ（黒次郎）
- リポ: kohtaro-preview-hub / protardesign（GitHub Pages・noindex）
- 関連: 本社 kohtaro-anything の design-stock

## 確定事項

- **屋号/ブランド**: ProtarDesign（プロターデザイン）。代表 井上浩太郎。**拠点＝神奈川県**（※当初「愛知」と誤記→全案修正済み）
- **事業の位置づけ**: 個人クリエイティブスタジオ。3本柱 ＝ ①ホームページ制作 ②AI活用支援・受託開発 ③自社プロダクト開発
  - つなぐたすける土木（つなたす）とは**別ブランドで並列**。サイトには「制作実績」として1本だけ掲載
  - 実績: プリポケ（PrintPocket）＋ つなたす
- **確定デザイン**: グラファイト(グレー金属)基調 × ティール(青緑 #0099b2) × ほんのり薄ローズ(#d693a8)。オーロラ・グラスモーフィズム
  - 本番ファイル: `protardesign/site.html`（原本 `proto-h14-graphite-teal-rose2.html`）
- **確定ロゴ**: 角丸スクエア・白地・"Protar"/"Design" 2段左揃え・中央罫線・Fraunces・ティールグラデ文字
  - `brand/logo-icon.svg`（標準）/ `brand/logo-icon-small.svg`（32px以下堅牢版・濃ティール単色 #007a91）/ `brand/logo-final.html`（ガイド）

## 検討経緯（要約）

1. 最初はプリポケ実績ハブとして作成 → 事業紹介サイトへ方針転換
2. デザイン案 A〜H を生成（暖色明朝/ダーク金/スイス/有機/和モダン/ターミナル/バウハウス/オーロラグラス）
3. 黒次郎・浩太郎の評価でオーロラグラス(H)が本命に。浩太郎の好み傾向＝「明るい・モダン・分かりやすい」、渋い/個性派は刺さりにくい
4. H のカラバリ多数（ocean/sunset/forest/dusk/mono、Apple風 silver-blue/graphite/midnight/starlight）→ グラファイト×ブルーを起点に、青→青緑、薄ローズ追加で微調整 → H14 確定
5. ロゴ探索4ページ（explorations / sns-icons / pd-variations / square-type）→ スクエア・フォントのみの「Protar/Design 2段左揃え・白地グラデ・中央罫線」を確定

## 公開URL（GitHub Pages・noindex）

- 確定サイト: https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/protardesign/site.html
- セレクト画面（全案）: https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/protardesign/
- ロゴガイド: https://kohtaroinoue-maker.github.io/kohtaro-preview-hub/protardesign/brand/logo-final.html

## 成果物の保存先

- preview-hub: `protardesign/`（site.html / brand/ / proto-*・logo-* 記録 / README.md）— push済
- 本社 design-stock: `memo/topics/design-stock/styles/graphite-teal-rose.css`（評価5/5）— push済
- Google Drive: ロゴSVGを「ProtarDesign」フォルダに格納（2026-05-28）

## 未了・次にやれること

- ロゴSVGのテキストはパス化していない（Fraunces webフォント前提）。印刷・確実な字形固定が要るならアウトライン化 or PNG/各サイズ書き出し
- 本番ドメイン取得・正式公開（現状はプレビューのみ noindex）は未着手
- メモリ化候補: ProtarDesignブランド確定 / 神奈川拠点 / design-stock運用（本ログ作成時点で浩太郎に提案中）
