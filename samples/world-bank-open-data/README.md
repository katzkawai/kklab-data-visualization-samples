# World Bank Open Data サンプルスクリプト

## fetch_gdp_per_capita.py

World Bank API から日本・アメリカ・中国の一人当たりGDP(2000〜2020年)を取得し、`gdp_per_capita.csv` に保存する。

```bash
python3 fetch_gdp_per_capita.py
```

- 標準ライブラリのみで動作(追加インストール不要)
- 取得先: `https://api.worldbank.org/v2/country/{国}/indicator/NY.GDP.PCAP.CD`

詳細は [World Bank Open Data チュートリアル](../../world-bank-open-data-tutorial.md) を参照。
