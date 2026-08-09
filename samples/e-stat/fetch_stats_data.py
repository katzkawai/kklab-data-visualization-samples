#!/usr/bin/env python3
"""e-Stat 統計データAPI で統計表を検索し、データを取得するサンプル。

使い方:
    1. https://www.e-stat.go.jp/api/ でアプリケーションID(appId)を取得
    2. 環境変数 ESTAT_APP_ID に設定
    3. python3 fetch_stats_data.py [検索キーワード]

標準ライブラリのみで動作する。
"""

import csv
import json
import os
import sys
import urllib.parse
import urllib.request

BASE_URL = "https://api.e-stat.go.jp/rest/3.0/app/json"
OUTPUT_CSV = "estat_data.csv"


def call_api(endpoint: str, params: dict) -> dict:
    """e-Stat APIを呼び出してJSONレスポンスを返す。"""
    url = f"{BASE_URL}/{endpoint}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read())


def search_stats_list(app_id: str, keyword: str) -> None:
    """キーワードで統計表を検索し、statsDataIdとタイトルを表示する。"""
    data = call_api(
        "getStatsList",
        {"appId": app_id, "searchWord": keyword, "limit": 10},
    )
    tables = (
        data.get("GET_STATS_LIST", {})
        .get("DATALIST_INF", {})
        .get("TABLE_INF", [])
    )
    if isinstance(tables, dict):
        tables = [tables]
    if not tables:
        print("該当する統計表が見つかりませんでした")
        return
    print("見つかった統計表:")
    for t in tables:
        print(f"  {t['@id']}  {t['TITLE']}")
    print("\n次に実行:")
    print(f"  python3 {sys.argv[0]} --data {tables[0]['@id']}")


def fetch_stats_data(app_id: str, stats_data_id: str) -> None:
    """statsDataIdを指定して統計データを取得し、CSVに保存する。"""
    data = call_api(
        "getStatsData",
        {
            "appId": app_id,
            "statsDataId": stats_data_id,
            "limit": 1000,
        },
    )
    values = (
        data.get("GET_STATS_DATA", {})
        .get("STATISTICAL_DATA", {})
        .get("DATA_INF", {})
        .get("VALUE", [])
    )
    if isinstance(values, dict):
        values = [values]
    if not values:
        print("データが取得できませんでした")
        return

    # キーを '@' なしにそろえてフラットなCSVにする
    rows = [{k.lstrip("@"): v for k, v in entry.items()} for entry in values]
    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} 件を {OUTPUT_CSV} に保存しました")
    for row in rows[:5]:
        print(row)


def main() -> None:
    app_id = os.environ.get("ESTAT_APP_ID")
    if not app_id:
        sys.exit(
            "エラー: 環境変数 ESTAT_APP_ID が設定されていません。\n"
            "https://www.e-stat.go.jp/api/ でアプリケーションIDを取得してください。"
        )

    args = sys.argv[1:]
    if args and args[0] == "--data" and len(args) == 2:
        fetch_stats_data(app_id, args[1])
    else:
        keyword = args[0] if args else "労働力調査"
        search_stats_list(app_id, keyword)


if __name__ == "__main__":
    main()
