# 2026-06-01 ProtarDesign ロゴ PNG 化 / アウトライン化（未完了）

## 経緯

ユーザー依頼: SVG しかない ProtarDesign ロゴの PNG を作って、Google Drive と
GitHub に置きたい。「ダブルスタンダードにしたくない」「PNG どれが正?」と問われ、
正のPNGを作る方針で進めたが、**フォント未解決によるレンダリング不正**が判明し、
**アウトライン化版 SVG を「正」とする運用** に切り替えた。
反映の途中で作業終了。

## 入力 SVG（既存・正）

`brand/logo-icon.svg` — primary（32px 超で使う本来版）
  - Fraunces wght 500、グラデ #3a4853→#0c8aa0→#0099b2、字間 0.2、罫線 50% 透過
`brand/logo-icon-small.svg` — small（32px 以下用の堅牢版）
  - Fraunces wght 600、単色 #007a91、字間 0、罫線 1.4px 不透明

両者は同一ブランドの **サイズ別バリアント**（ダブルスタンダードではない）。
- ≥ 48px: icon
- ≤ 32px: icon-small（favicon 等）

## やったこと

1. `brew install librsvg` — `rsvg-convert` 導入
2. SVG → PNG 6枚を `brand/png/` に生成（icon × 512/1024/2048、small × 同）
3. ローカル GoogleDrive 同期フォルダ `~/Library/CloudStorage/GoogleDrive-.../マイドライブ/ProtarDesign/png/` にコピー
4. GitHub に push（commit `9354a2d Add ProtarDesign ロゴ PNG`）

## ここで発覚した問題（重要）

- `rsvg-convert` は SVG 内の `@import url(Google Fonts)` を解決しない（ネットに取りに行かない）。
- Mac に Fraunces が入っていなかったので、PNG は **両方とも Georgia/serif にフォールバック** して描画された。
- weight 500 vs 600 の差で「フォントが違う気がする」と見えたのはこのため。
- → **GitHub の `9354a2d` で push した 6 PNG は字形が Fraunces ではなく不正**。

SVG コメントに設計者本人が書いていた:
> ※ 印刷・アイコン埋め込み等で確実に字形を固定したい場合は、別途このSVGのテキストをアウトライン化してください。

これがそのまま正解だった。

## 採用した解決策（B案: アウトライン化）

1. `brew install --cask font-fraunces` で Fraunces Variable をインストール。
2. `python3 -m pip install fonttools brotli` で fonttools を準備（mise Python 3.13）。
3. アウトライン化スクリプト `brand/_tools/outline_logo.py` を作成。
   - `varLib.mutator.instantiateVariableFont` で wght=500 / 600 にインスタンス化
   - 各文字を `SVGPathPen` で path 化、`<text>` を `<g><path/></g>` に置換
   - `dominant-baseline="central"` → SVG baseline = y + (asc+desc)/2 * scale で換算
4. 出力:
   - `brand/logo-icon-outlined.svg`
   - `brand/logo-icon-small-outlined.svg`
5. アウトライン版 SVG から `brand/png-new/` に PNG 6枚を再生成。
6. 視覚確認 OK（Fraunces のセリフ・`g` のループ・`D` の終端が出ている）。

## 現状（途中で停止）

| アイテム | 状態 |
|---|---|
| `brand/logo-icon-outlined.svg` | 生成済（**未 commit**） |
| `brand/logo-icon-small-outlined.svg` | 生成済（**未 commit**） |
| `brand/_tools/outline_logo.py` | 生成済（**未 commit**） |
| `brand/png-new/` 6 PNG（Fraunces 正） | 生成済（**未 commit**、まだ `png/` に未反映） |
| `brand/png/` 6 PNG（Georgia 不正） | **GitHub に push 済**（`9354a2d`）。ローカル / Drive 同期にも残存 |
| Google Drive 同期 `ProtarDesign/png/` | 不正 PNG が同期済 |

## 再開時の手順（未完了タスク）

1. 入れ替え:
   ```bash
   cd ~/dev/kohtaro-preview-hub/protardesign/brand
   rm -rf png
   mv png-new png
   ```
2. Google Drive 同期側も差し替え:
   ```bash
   DEST="$HOME/Library/CloudStorage/GoogleDrive-kohtaro.inoue@gmail.com/マイドライブ/ProtarDesign/png"
   rm -rf "$DEST"
   cp -r ~/dev/kohtaro-preview-hub/protardesign/brand/png "$DEST"
   ```
3. git に反映（`*-outlined.svg`, `_tools/outline_logo.py`, `png/` 差し替えをまとめて）:
   ```bash
   cd ~/dev/kohtaro-preview-hub
   git add protardesign/brand/logo-icon-outlined.svg \
           protardesign/brand/logo-icon-small-outlined.svg \
           protardesign/brand/_tools/outline_logo.py \
           protardesign/brand/png/
   git commit -m "Fix ProtarDesign logo PNG: outline (Fraunces) で再生成、不正 Georgia 版を差し替え"
   git push
   ```
4. 元の Web フォント版 SVG（`logo-icon.svg` / `logo-icon-small.svg`）は **残す**:
   - HTML 用には Web フォントで読み込ませる版がベスト（文字編集可能）
   - アウトライン版は埋め込み・印刷・PNG 化の素材として共存させる

## 判断保留 / 次回ユーザー確認事項

- [ ] `small` の PNG は 512/1024/2048 を作ったが、本来 small は ≤ 32px 用。
      正の運用としては **small の PNG は 16/32/48 に絞る** べきでは。
      今回は揃えて作ったが、いずれ判断要。
- [ ] `_tools/outline_logo.py` を git に含めるか（再生成手順として残す価値あり）。
      今回は「含める」で書いてあるが、ユーザー確認したい場合は再開時に。
- [ ] `_handover/` 自体は引き続き untracked（既存運用維持）。

## 参考: 環境変化

- `brew install librsvg`（依存込で大量に導入、`rsvg-convert 2.62.2`）
- `brew install --cask font-fraunces`（Variable TTF を `~/Library/Fonts/` に配置）
- `python3 -m pip install fonttools brotli`（mise Python 3.13 にユーザーインストール）

## 関連

- 前回ログ: `2026-05-28-protardesign-site-logo.md`（ロゴ確定と site への組込み）
- 関連 commit: `8d2d44e`（事業紹介サイト確定＋ロゴ追加）, `9354a2d`（不正 PNG push, **要差し替え**）
