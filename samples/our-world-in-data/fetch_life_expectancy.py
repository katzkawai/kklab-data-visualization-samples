#!/usr/bin/env python3
"""Our World in Data の Grapher API から平均寿命データを取得するサンプル。

標準ライブラリのみで動作する。
"""

import csv
import urllib.request

SLUG = "life-expectancy"  # グラフページのURLから確認できるスラッグ
URL = f"https://ourworldindata.org/grapher/{SLUG}.csv"
OUTPUT_CSV = "life_expectancy.csv"
TARGET_COUNTRY = "Japan"  # サマリ表示の対象国


def main() -> None:
    # CSVをダウンロード(デフォルトのUser-Agentでは403になるためブラウザ風に設定)
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req) as res:
        text = res.read().decode("utf-8")

    with open(OUTPUT_CSV, "w") as f:
        f.write(text)

    rows = list(csv.DictReader(text.splitlines()))
    print(f"{len(rows)} 件を {OUTPUT_CSV} に保存しました")
    print(f"列: {list(rows[0].keys())}")

    # 対象国のデータだけ抽出して最新5件を表示
    country_rows = [r for r in rows if r["Entity"] == TARGET_COUNTRY]
    country_rows.sort(key=lambda r: r["Year"])
    value_col = next(c for c in rows[0] if c not in ("Entity", "Code", "Year"))
    print(f"\n{TARGET_COUNTRY} の最新5件:")
    for r in country_rows[-5:]:
        print(f"  {r['Year']}: {r[value_col]}")


if __name__ == "__main__":
    main()
