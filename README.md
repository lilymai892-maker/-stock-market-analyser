# Stock Market & Financial Analyzer

A Python + SQL project that fetches real company financial data, stores it in a structured database, calculates key audit ratios, and automatically flags anomalies — mirroring data-driven audit workflows used by Big 4 firms.

![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat-square&logo=python)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey?style=flat-square&logo=sqlite)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?style=flat-square&logo=pandas)
![Matplotlib](https://img.shields.io/badge/Matplotlib-Charts-orange?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## What It Does

- **Stores** structured financial data in a local SQLite database
- **Calculates** key audit ratios: Gross Margin, Net Margin, Return on Assets, Return on Equity, and Leverage Ratio
- **Detects anomalies** automatically — sharp margin drops, high leverage, revenue declines, and net losses
- **Visualizes** trends with 9 professional charts saved to the reports/ folder

---

## Project Structure

```
stock-market-analyzer/
│
├── main.py                  # Entry point — runs the full pipeline
├── requirements.txt
├── README.md
├── database/
│   └── setup.py             # Creates and initializes the SQLite DB
├── analysis/
│   ├── loader.py            # Loads financial + price data into DB
│   └── queries.py           # SQL queries to compute ratios & detect anomalies
└── reports/
    └── report.py            # Generates charts with matplotlib
```

---

## Setup & Installation

**1. Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/stock-market-analyzer.git
cd stock-market-analyzer
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Run the analyzer**
```bash
python main.py
```

---

## Requirements

```
pandas>=1.5.0
matplotlib>=3.5.0
yfinance>=0.2.0
```

---

## How It Works

### 1. Database Storage
Data is stored in a local SQLite database with three core tables:

| Table | Description |
|---|---|
| `companies` | Ticker, name, sector, industry |
| `daily_prices` | Open, high, low, close, volume per day |
| `financials` | Revenue, gross profit, net income, assets, liabilities, equity per year |

### 2. Ratio Calculation (via SQL)
Key ratios are computed using SQL queries:

| Ratio | Formula |
|---|---|
| Gross Margin % | `Gross Profit / Revenue × 100` |
| Net Margin % | `Net Income / Revenue × 100` |
| Return on Assets % | `Net Income / Total Assets × 100` |
| Return on Equity % | `Net Income / Equity × 100` |
| Leverage Ratio | `Total Assets / Equity` |

### 3. Anomaly Detection
The analyzer automatically flags:
- Gross margin drop of more than **5 percentage points** year-over-year
- Leverage ratio exceeding **4x** (high debt risk)
- Revenue decline of more than **5%** year-over-year
- Any year with a **net loss**

---

## Sample Output

```
=== Financial Ratios ===
ticker  year  gross_margin_pct  net_margin_pct  roa_pct  leverage_ratio
  AAPL  2020             38.23           20.91    17.73            4.96
  AAPL  2021             41.78           25.88    26.97            5.56
  AMZN  2022             36.48           -0.53    -0.59            3.17
  TSLA  2023             18.25           15.47    14.04            1.70

=== Anomaly Flags ===
🔴 [AAPL 2021] High leverage ratio: 5.56x
⚠️  [AMZN 2022] Gross margin dropped 5.6pp
🔴 [AMZN 2022] Net loss recorded: $-2,722M
⚠️  [TSLA 2023] Gross margin dropped 7.4pp
```

---

## Charts Generated

| Chart | Description |
|---|---|
| `AAPL_price_ma.png` | Price history with 50 & 200-day moving averages |
| `ratio_comparison.png` | Side-by-side ratio comparison across all companies |
| `margin_trends.png` | Gross & net margin trends over time |
| `revenue_growth.png` | Stacked revenue bar chart by company |
| `anomaly_flags.png` | Visual table of all detected audit flags |

---

## Relevance to Audit

This project replicates core techniques used in modern audit practice:

- **Analytical procedures** — comparing ratios across periods to identify unusual fluctuations (ISA 520)
- **Risk assessment** — flagging high leverage and margin deterioration as indicators of financial stress
- **Data-driven audit** — using structured databases and automated queries instead of manual spreadsheet review


---

## Author

**Nguyen Quynh Anh Mai**
- LinkedIn: https://www.linkedin.com/in/lily-m-b32bb3298/
- Email: lily.mai892@gmail.com
---

## License

This project is licensed under the MIT License.
