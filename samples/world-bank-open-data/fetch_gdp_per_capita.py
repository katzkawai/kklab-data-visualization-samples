#!/usr/bin/env python3
"""World Bank Open Data API から一人当たりGDPを取得してCSVに保存するサンプル。

標準ライブラリのみで動作する。
"""

import csv
import json
import urllib.request

COUNTRIES = ["JPN", "USA", "CHN"]
INDICATOR = "NY.GDP.PCAP.CD"  # 一人当たりGDP(米ドル)
START_YEAR = 2000
END_YEAR = 2020
OUTPUT_CSV = "gdp_per_capita.csv"


def fetch(country: str, indicator: str, start: int, end: int) -> list[dict]:
    """指定国・指標・期間のデータをWorld Bank APIから取得する。"""
    url = (
        f"https://api.worldbank.org/v2/country/{country}"
        f"/indicator/{indicator}"
        f"?format=json&date={start}:{end}&per_page=500"
    )
    with urllib.request.urlopen(url) as res:
        payload = json.loads(res.read())
    # レスポンスは [メタ情報, データ配列] の2要素
    if not isinstance(payload, list) or len(payload) < 2 or payload[1] is None:
        raise RuntimeError(f"データが取得できませんでした: {country}")
    return payload[1]


def main() -> None:
    rows = []
    for country in COUNTRIES:
        for entry in fetch(country, INDICATOR, START_YEAR, END_YEAR):
            rows.append(
                {
                    "country": entry["countryiso3code"],
                    "year": entry["date"],
                    "value": entry["value"],
                }
            )

    rows.sort(key=lambda r: (r["country"], r["year"]))

    with open(OUTPUT_CSV, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["country", "year", "value"])
        writer.writeheader()
        writer.writerows(rows)

    print(f"{len(rows)} 件を {OUTPUT_CSV} に保存しました")
    for row in rows[:5]:
        print(row)


if __name__ == "__main__":
    main()
