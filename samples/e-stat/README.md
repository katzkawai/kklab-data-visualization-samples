# e-Stat サンプルスクリプト

## fetch_stats_data.py

e-Stat 統計データAPI で統計表を検索し、指定した統計表のデータを `estat_data.csv` に保存する。

### 事前準備

1. <https://www.e-stat.go.jp/api/> でアプリケーションID(appId)を取得(無料・要登録)
2. 環境変数に設定:

```bash
export ESTAT_APP_ID="あなたのappId"
```

### 使い方

```bash
# 統計表を検索(statsDataIdの一覧を表示)
python3 fetch_stats_data.py 労働力調査

# データを取得してCSVに保存
python3 fetch_stats_data.py --data STATS_DATA_ID
```

- 標準ライブラリのみで動作(追加インストール不要)
- APIが無い環境では実行できない点に注意

詳細は [e-Stat チュートリアル](../../e-stat-tutorial.md) を参照。
