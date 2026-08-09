# Our World in Data チュートリアル

オックスフォード大学発の研究プロジェクトが運営する **Our World in Data**(<https://ourworldindata.org/>)の使い方とデータの入手方法を説明する。

## データの概要

- 世界銀行・国連・WHO・OECDなどの一次データを加工・統合し、トピック別に整理して公開
- 貧困・所得格差、健康・死亡率、エネルギー・環境、人口・移住、戦争・紛争、幸福度、民主主義など幅広い
- 長期時系列(数百年に及ぶものも)の国際比較データが充実
- ライセンスは CC BY 4.0(出典明記で自由に利用可能)

## 入手方法1: Webサイトからダウンロード

1. <https://ourworldindata.org/> にアクセス
2. トピック一覧(「Topics」)または検索で目的の指標を探す
3. 各グラフのページで「Download」タブを開く
4. **CSV** でデータをダウンロード(画像としてのエクスポートも可能)

CSVには国名(Entity)、国コード(Code)、年(Year)、指標値の列が含まれ、すぐに分析に使える整形済みの形式になっている。

## 入手方法2: Grapher API

サイト上の各グラフ(チャート)には固有のスラッグ(識別子)があり、URLを直接叩くと CSV / JSON / メタデータを取得できる。

### 基本形式

```
https://ourworldindata.org/grapher/{スラッグ}.csv
https://ourworldindata.org/grapher/{スラッグ}.json
https://ourworldindata.org/grapher/{スラッグ}.metadata.json
```

スラッグはグラフページのURLから確認できる(例: `ourworldindata.org/grapher/life-expectancy` → `life-expectancy`)。

### 例: 平均寿命データのCSV取得

```bash
curl -o life-expectancy.csv "https://ourworldindata.org/grapher/life-expectancy.csv"
```

### クエリパラメータ

- `time=2000..2020` — 期間の絞り込み
- `country=~JPN` — 国の絞り込み
- `useColumnShortNames=true` — 列名を短くする
- `csvType=filtered` — グラフ上で選択された系列のみ取得

```bash
# 日本のデータだけ、2000年以降
curl "https://ourworldindata.org/grapher/life-expectancy.csv?time=2000..latest&country=~JPN"
```

### Pythonからの利用

```python
import pandas as pd

url = "https://ourworldindata.org/grapher/life-expectancy.csv"
df = pd.read_csv(url)
print(df.head())
```

## 入手方法3: GitHub / カタログ

- **Grapher データのGitHubミラー**: <https://github.com/owid/owid-grapher-svgs> など、関連リポジトリは <https://github.com/owid> に集約されている
- **ETLカタログ**: <https://catalog.ourworldindata.org/> でデータセットを横断検索できる。より厳密なデータ取得には Python パッケージ `owid-catalog` を使う方法もある

## 代表的なスラッグ例

| スラッグ | 内容 |
| --- | --- |
| `life-expectancy` | 出生時平均余命 |
| `gdp-vs-happiness` | 一人当たりGDPと幸福度 |
| `income-inequality` | 所得格差 |
| `co2-emissions-per-capita` | 一人当たりCO2排出量 |
| `share-of-population-in-extreme-poverty` | 極度の貧困率 |

スラッグが分からない場合は、サイト上の該当グラフのページを開きURLを確認するのが確実。

## 注意点

- データは一次出典(World Bank、WHOなど)の更新に追随するため、更新頻度は指標によって異なる
- 同じ指標でも加工方法が出典元と異なる場合がある。ページに記載される出典・定義のメタデータを確認すること
- `.metadata.json` には出典、単位、加工方法の説明が含まれるので、引用時に参照するとよい

## 関連

- [データビジュアライゼーションとは](data-visualization.md)
- [World Bank Open Data チュートリアル](world-bank-open-data-tutorial.md)
- [e-Stat チュートリアル](e-stat-tutorial.md)
- サンプルスクリプト: [samples/our-world-in-data/](samples/our-world-in-data/)
- 公式ドキュメント: <https://docs.owid.io/>
