# e-Stat(日本政府統計)チュートリアル

総務省統計局が運営する政府統計の総合窓口 **e-Stat**(<https://www.e-stat.go.jp/>)の使い方とデータの入手方法を説明する。

## データの概要

- 日本の各省庁が実施する統計調査の結果を横断的に検索・閲覧できるポータル
- 国勢調査(5年ごと)、人口推計、人口動態調査、労働力調査、家計調査、経済センサス、学校基本調査、犯罪統計など
- ライセンス: 政府標準利用規約に準拠(出典明記で転載・複製・改変が可能)

## 入手方法1: Webサイトからダウンロード

1. <https://www.e-stat.go.jp/> にアクセス
2. 「統計データを探す」から統計分野(人口・世帯、労働・賃金など)またはキーワードで検索
3. 統計表のページで条件(地域、期間、項目)を選択
4. **CSV / Excel / PDF** 形式でダウンロード

CSVの文字コードは Shift_JIS の場合があるため、Pythonで読む際はエンコーディング指定に注意する。

```python
import pandas as pd

df = pd.read_csv("downloaded.csv", encoding="shift_jis")
```

## 入手方法2: 統計データAPI

APIの利用には無料の**アプリケーションID(appId)** の登録が必要。

### 1. アプリIDの取得

1. <https://www.e-stat.go.jp/api/> にアクセス
2. 利用者登録・API利用申請を行う
3. 発行された appId を控える

### 2. APIの基本

ベースURL:

```
https://api.e-stat.go.jp/rest/3.0/app/json/
```

主なエンドポイント:

| エンドポイント | 用途 |
| --- | --- |
| `getStatsList` | 統計表の検索(政府統計の一覧) |
| `getMetaInfo` | 統計表のメタ情報(項目・分類の定義)取得 |
| `getStatsData` | 統計データ本体の取得 |

### 3. 統計表を検索する(getStatsList)

```bash
curl "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList?appId=YOUR_APP_ID&searchWord=国勢調査"
```

結果に含まれる `@id`(statsDataId)を使って次のステップに進む。

### 4. メタ情報を確認する(getMetaInfo)

```bash
curl "https://api.e-stat.go.jp/rest/3.0/app/json/getMetaInfo?appId=YOUR_APP_ID&statsDataId=STATS_DATA_ID"
```

統計表が持つ分類(地域、年齢、男女など)と各コードの対応が返る。データ取得時の絞り込み条件(cdArea、cdCat01など)はここで確認する。

### 5. データを取得する(getStatsData)

```bash
curl "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData?appId=YOUR_APP_ID&statsDataId=STATS_DATA_ID&limit=1000"
```

主なパラメータ:

- `limit` — 取得件数(デフォルトは最大10万件)
- `startPosition` — ページングの開始位置
- `cdArea`、`cdTime` など — メタ情報で確認した分類コードによる絞り込み
- `metaGetFlg=N` — メタ情報を省略して応答を軽くする

### Pythonからの利用

```python
import requests
import pandas as pd

APP_ID = "YOUR_APP_ID"

# 1. 統計表を検索
res = requests.get(
    "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsList",
    params={"appId": APP_ID, "searchWord": "労働力調査", "limit": 10},
).json()
tables = res["GET_STATS_LIST"]["DATALIST_INF"]["TABLE_INF"]
for t in tables:
    print(t["@id"], t["TITLE"])

# 2. データを取得してDataFrame化
res = requests.get(
    "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData",
    params={"appId": APP_ID, "statsDataId": "STATS_DATA_ID", "limit": 1000},
).json()
values = res["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"]["VALUE"]
df = pd.DataFrame(values)
print(df.head())
```

JSONの構造は階層が深いため、実際のレスポンスを一度確認してからパース処理を書くのが確実。

## 入手方法3: 地図で見る統計(jSTAT MAP)

<https://jstatmap.e-stat.go.jp/> では、国勢調査などのデータを市区町村・町丁字・メッシュ単位で地図上に可視化できる。GISデータ(Shapefile)のダウンロードも可能で、地域分布の可視化に向いている。

## 注意点

- **APIキー(appId)は必須**。未取得の場合はWebダウンロードのみ利用可能
- データは二次加工しやすいよう、CSVのヘッダー行やメタ情報の扱いに注意(統計表によってフォーマットが異なる)
- 国勢調査以外の調査は実施周期がまちまち(毎月、毎年、5年ごとなど)なので、時系列分析では調査周期を確認する
- 統計表ごとに「利用上の注意」が用意されている。調査方法や推計の有無を確認してから分析に使うこと

## 関連

- [データビジュアライゼーションとは](data-visualization.md)
- [World Bank Open Data チュートリアル](world-bank-open-data-tutorial.md)
- [Our World in Data チュートリアル](our-world-in-data-tutorial.md)
- サンプルスクリプト: [samples/e-stat/](samples/e-stat/)
- 公式API仕様: <https://www.e-stat.go.jp/api/api-info/api-spec>
