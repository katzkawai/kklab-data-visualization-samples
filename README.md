# kklab-data-visualization-samples

データビジュアライゼーションの学習用リポジトリです。公開データ(World Bank Open Data、Our World in Data、e-Stat)の入手方法のチュートリアルと、取得したデータを可視化するサンプルを収録しています。

このリポジトリは **Kimi K3** を使って作成されました。

## 公開ページ

<https://katzkawai.org/kklab-data-visualization-samples/>

サンプルスクリプトで取得したデータを Chart.js で可視化したデモページです(GitHub Pages で公開)。

- 一人当たりGDPの推移(World Bank Open Data)
- 平均寿命の推移(Our World in Data) — 急減箇所の背景解説付き

## チュートリアル

- [データビジュアライゼーションとは](data-visualization.md) — 概要と社会科学分野の題材、公開データの紹介
- [World Bank Open Data チュートリアル](world-bank-open-data-tutorial.md) — REST API / Pythonライブラリでのデータ取得
- [Our World in Data チュートリアル](our-world-in-data-tutorial.md) — Grapher API / CSV でのデータ取得
- [e-Stat チュートリアル](e-stat-tutorial.md) — 日本政府統計の検索・統計データAPIの利用

## サンプルスクリプト

`samples/` 以下に、標準ライブラリのみで動作するデータ取得スクリプトがあります。

| ディレクトリ | 内容 |
| --- | --- |
| [samples/world-bank-open-data/](samples/world-bank-open-data/) | 日米中の一人当たりGDPを取得してCSV保存 |
| [samples/our-world-in-data/](samples/our-world-in-data/) | 平均寿命データをCSV取得・要約表示 |
| [samples/e-stat/](samples/e-stat/) | 統計表の検索とデータ取得(要アプリケーションID) |

## ライセンス

各データセットのライセンスは取得元の条件に従います(World Bank Open Data・Our World in Data は CC BY 4.0、e-Stat は政府標準利用規約)。
