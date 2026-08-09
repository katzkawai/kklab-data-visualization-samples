# Our World in Data サンプルスクリプト

## fetch_life_expectancy.py

Grapher API から平均寿命データをCSVでダウンロードし、`life_expectancy.csv` に保存したあと、日本の最新5件を表示する。

```bash
python3 fetch_life_expectancy.py
```

- 標準ライブラリのみで動作(追加インストール不要)
- 取得先: `https://ourworldindata.org/grapher/life-expectancy.csv`

詳細は [Our World in Data チュートリアル](../../our-world-in-data-tutorial.md) を参照。
