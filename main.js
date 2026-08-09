// サンプルスクリプトで取得したCSVを読み込み、Chart.jsで可視化する。

const GDP_CSV = "samples/world-bank-open-data/gdp_per_capita.csv";
const LIFE_CSV = "samples/our-world-in-data/life_expectancy.csv";

const COUNTRY_NAMES = {
  JPN: "日本",
  USA: "アメリカ",
  CHN: "中国",
  Japan: "日本",
  "United States": "アメリカ",
  China: "中国",
  World: "世界",
};

const COLORS = ["#e15759", "#4e79a7", "#59a14f", "#f28e2b"];

// クォート対応の簡易CSVパーサ
function parseCsv(text) {
  const rows = [];
  let row = [];
  let field = "";
  let inQuotes = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
    } else if (c === '"') {
      inQuotes = true;
    } else if (c === ",") {
      row.push(field);
      field = "";
    } else if (c === "\n" || c === "\r") {
      if (c === "\r" && text[i + 1] === "\n") i++;
      row.push(field);
      field = "";
      if (row.length > 1 || row[0] !== "") rows.push(row);
      row = [];
    } else {
      field += c;
    }
  }
  if (field !== "" || row.length > 0) {
    row.push(field);
    rows.push(row);
  }
  const [header, ...data] = rows;
  return data.map((r) => Object.fromEntries(header.map((h, i) => [h, r[i]])));
}

// 国ごとに {年: 値} の系列にまとめ、年の昇順でChart.js用データを返す
function toDatasets(rows, countryKey, yearKey, valueKey, countries) {
  return countries
    .map((country, idx) => {
      const points = rows
        .filter((r) => r[countryKey] === country && r[valueKey] !== "" && r[valueKey] != null)
        .map((r) => ({ x: Number(r[yearKey]), y: Number(r[valueKey]) }))
        .sort((a, b) => a.x - b.x);
      return {
        label: COUNTRY_NAMES[country] || country,
        data: points,
        borderColor: COLORS[idx % COLORS.length],
        backgroundColor: COLORS[idx % COLORS.length],
        tension: 0.2,
        pointRadius: 0,
      };
    })
    .filter((d) => d.data.length > 0);
}

async function fetchCsv(url) {
  const res = await fetch(url);
  if (!res.ok) throw new Error(`${url} の取得に失敗しました (${res.status})`);
  return parseCsv(await res.text());
}

function drawLineChart(canvasId, datasets, xTitle, yTitle) {
  new Chart(document.getElementById(canvasId), {
    type: "line",
    data: { datasets },
    options: {
      scales: {
        x: { type: "linear", title: { display: true, text: xTitle } },
        y: { title: { display: true, text: yTitle } },
      },
      interaction: { mode: "nearest", intersect: false },
    },
  });
}

async function main() {
  // 一人当たりGDP(World Bank)
  const gdpRows = await fetchCsv(GDP_CSV);
  drawLineChart(
    "gdpChart",
    toDatasets(gdpRows, "country", "year", "value", ["JPN", "USA", "CHN"]),
    "年",
    "一人当たりGDP(米ドル)"
  );

  // 平均寿命(Our World in Data)
  const lifeRows = await fetchCsv(LIFE_CSV);
  drawLineChart(
    "lifeChart",
    toDatasets(lifeRows, "Entity", "Year", "Life expectancy", [
      "Japan",
      "United States",
      "China",
      "World",
    ]),
    "年",
    "出生時平均余命(歳)"
  );
}

main().catch((err) => {
  document.body.insertAdjacentHTML(
    "afterbegin",
    `<p style="color:red">データの読み込みに失敗しました: ${err.message}</p>`
  );
});
