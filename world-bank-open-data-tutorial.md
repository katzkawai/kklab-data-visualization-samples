# World Bank Open Data チュートリアル

世界銀行が公開する開発指標データベース **World Bank Open Data**(<https://data.worldbank.org/>)の使い方とデータの入手方法を説明する。

## データの概要

- 中核データベースは **WDI(World Development Indicators)**
- 200以上の国・地域、1960年代から現在までの1,400以上の指標
- 経済(GDP、GNI、インフレ)、人口(出生率、平均寿命)、教育(識字率、就学率)、環境(CO2排出量)など
- ライセンスは CC BY 4.0(出典明記で自由に利用可能)

## 入手方法1: Webサイトからダウンロード

1. <https://data.worldbank.org/> にアクセス
2. 「Indicators」から指標を検索(例: `GDP per capita`、日本語UIも選択可能)
3. 指標ページで国・期間を選択
4. 「Download」ボタンから **CSV / Excel / XML** 形式でダウンロード

複数の指標をまとめて取得したい場合は、「DataBank」(<https://databank.worldbank.org/>)でデータベース・国・指標・期間を組み合わせてカスタム抽出できる。

## 入手方法2: REST API

登録不要・無料の REST API が用意されている。

### 基本形式

```
https://api.worldbank.org/v2/country/{国コード}/indicator/{指標コード}?format=json&date={開始年}:{終了年}
```

- **国コード**: ISO 3166-1 alpha-3(`JPN`、`USA`、`CHN` など)。`all` ですべての国。`JPN;USA;CHN` で複数指定も可能
- **指標コード**: 例えば `NY.GDP.PCAP.CD`(一人当たりGDP)、`SP.POP.TOTL`(総人口)、`SP.DYN.LE00.IN`(平均寿命)
- **format**: `json` または `xml`
- **date**: `2000:2020` のような範囲指定
- **per_page**: 1ページの件数(デフォルト50、大量取得時は `per_page=20000` など)

### 例: 日本の一人当たりGDP(2000〜2020年)

```bash
curl "https://api.worldbank.org/v2/country/JPN/indicator/NY.GDP.PCAP.CD?format=json&date=2000:2020&per_page=100"
```

レスポンスは `[メタ情報, データ配列]` の2要素のJSON配列で、各データは `countryiso3code`、`date`、`value` などのフィールドを持つ。

### 指標コードの調べ方

```bash
# 全指標一覧(ページングあり)
curl "https://api.worldbank.org/v2/indicator?format=json&per_page=100"
```

Webサイトの指標ページのURLからも確認できる(例: `.../indicator/NY.GDP.PCAP.CD`)。

## 入手方法3: Pythonライブラリ

### wbgapi

```bash
pip install wbgapi
```

```python
import wbgapi as wb

# 日本・アメリカ・中国の一人当たりGDPを2000〜2020年で取得
df = wb.data.DataFrame(
    'NY.GDP.PCAP.CD',
    ['JPN', 'USA', 'CHN'],
    range(2000, 2021),
)
print(df)
```

### pandas-datareader

```bash
pip install pandas-datareader
```

```python
from pandas_datareader import wb

df = wb.download(
    indicator='NY.GDP.PCAP.CD',
    country=['JP', 'US', 'CN'],
    start=2000,
    end=2020,
)
print(df.head())
```

## よく使う指標コード

| コード | 内容 |
| --- | --- |
| `NY.GDP.PCAP.CD` | 一人当たりGDP(米ドル) |
| `SP.POP.TOTL` | 総人口 |
| `SP.DYN.LE00.IN` | 出生時平均余命 |
| `SI.POV.GINI` | Gini係数 |
| `SE.ADT.LITR.ZS` | 成人識字率 |
| `EN.ATM.CO2E.PC` | 一人当たりCO2排出量 |

## 注意点

- 国によっては特定年のデータが欠損(`value` が `null`)していることが多い。可視化前に欠損値の処理が必要
- 最新データでも公表には1〜2年のタイムラグがある
- `date=2000:2020` の範囲指定のほか、`date=2020`(単年)や `mrv=5`(最新5件)も使える

## 関連

- [データビジュアライゼーションとは](data-visualization.md)
- [Our World in Data チュートリアル](our-world-in-data-tutorial.md)
- 公式APIドキュメント: <https://datahelpdesk.worldbank.org/knowledgebase/topics/125589-developer-information>
