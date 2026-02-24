"""
main.py — Stock Market & Financial Analyzer
============================================
A Python + SQL project that:
  1. Loads company stock price and financial data into SQLite
  2. Runs SQL queries to compute key financial ratios
  3. Detects audit anomalies automatically
  4. Generates professional charts saved to reports/

Run:
    python main.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from database.setup   import create_database
from analysis.loader  import load_data
from analysis.queries import get_financial_ratios, detect_anomalies, get_volatility_summary
from reports.report   import generate_all_reports


def print_header(title):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'═'*60}")


def main():
    print("\n🚀 Stock Market & Financial Analyzer")
    print("   Python + SQLite | Data Analysis Project\n")

    print_header("STEP 1 — Setting up database")
    create_database()

    print_header("STEP 2 — Loading data")
    load_data()

    print_header("STEP 3 — Financial Ratios (SQL Query Output)")
    ratios = get_financial_ratios()
    display_cols = ["ticker", "year", "gross_margin_pct", "net_margin_pct", "roa_pct", "leverage_ratio"]
    print(ratios[display_cols].to_string(index=False))

    print_header("STEP 4 — Anomaly Detection")
    flags = detect_anomalies()
    if flags.empty:
        print("  ✅ No anomalies detected.")
    else:
        for _, row in flags.iterrows():
            icon = "🔴" if row.severity == "DANGER" else "⚠️ "
            print(f"  {icon} [{row.ticker} {row.year}] {row.flag}")

    print_header("STEP 5 — Price Volatility Summary")
    vol = get_volatility_summary()
    print(vol.to_string(index=False))

    print_header("STEP 6 — Generating Charts")
    generate_all_reports()

    print("\n✅ Analysis complete!")
    print("   Open the reports/ folder to view your charts.\n")


if __name__ == "__main__":
    main()
```

