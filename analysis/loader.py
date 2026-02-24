import sqlite3
import pandas as pd
import random
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from database.setup import get_connection

COMPANIES = [
    {"ticker": "AAPL", "name": "Apple Inc.",       "sector": "Technology",   "industry": "Consumer Electronics"},
    {"ticker": "MSFT", "name": "Microsoft Corp.",   "sector": "Technology",   "industry": "Software"},
    {"ticker": "TSLA", "name": "Tesla Inc.",         "sector": "Automotive",   "industry": "Electric Vehicles"},
    {"ticker": "AMZN", "name": "Amazon.com Inc.",   "sector": "Consumer",     "industry": "E-Commerce"},
    {"ticker": "GOOGL","name": "Alphabet Inc.",     "sector": "Technology",   "industry": "Internet Services"},
]

FINANCIALS = {
    "AAPL":  [
        (2020, 274515, 104956, 57411, 323888, 258549, 65339),
        (2021, 365817, 152836, 94680, 351002, 287912, 63090),
        (2022, 394328, 170782, 99803, 352755, 302083, 50672),
        (2023, 383285, 169148, 96995, 352583, 290437, 62146),
    ],
    "MSFT":  [
        (2020, 143015, 96937, 44281, 301311, 183007, 118304),
        (2021, 168088, 115856, 61271, 333779, 191791, 141988),
        (2022, 198270, 135620, 72738, 364840, 198298, 166542),
        (2023, 211915, 146052, 72361, 411976, 205753, 206223),
    ],
    "TSLA":  [
        (2020,  31536,  6630,    721,  52148,  28170,  22225),
        (2021,  53823, 13606,   5519,  62131,  30548,  30189),
        (2022,  81462, 20853,  12556,  82338,  36440,  44704),
        (2023,  96773, 17660,  14974, 106618,  43009,  62634),
    ],
    "AMZN":  [
        (2020, 386064, 152757, 21331, 321195, 227791,  93404),
        (2021, 469822, 197478, 33364, 420549, 282304, 138245),
        (2022, 513983, 187506, -2722, 462675, 316932, 146043),
        (2023, 574785, 230849, 30425, 527854, 338206, 189648),
    ],
    "GOOGL": [
        (2020, 182527, 97795,  40269, 319616, 97072,  222544),
        (2021, 257637, 146698, 76033, 359268, 107633, 251635),
        (2022, 282836, 156633, 59972, 359268, 109120, 256144),
        (2023, 307394, 174062, 73795, 402392, 109120, 283379),
    ],
}

BASE_PRICES = {"AAPL": 130, "MSFT": 230, "TSLA": 220, "AMZN": 165, "GOOGL": 140}

def simulate_prices(ticker, start="2022-01-01", end="2024-01-01"):
    dates = pd.date_range(start=start, end=end, freq="B")
    price = BASE_PRICES[ticker]
    rows = []
    random.seed(hash(ticker) % 9999)
    drift = 0.0003
    volatility = 0.018
    for date in dates:
        ret = drift + volatility * random.gauss(0, 1)
        price = price * math.exp(ret)
        daily_vol = volatility * random.uniform(0.5, 1.5)
        high  = price * (1 + abs(random.gauss(0, daily_vol)))
        low   = price * (1 - abs(random.gauss(0, daily_vol)))
        open_ = low + random.random() * (high - low)
        volume = int(random.uniform(20e6, 120e6))
        rows.append((date.strftime("%Y-%m-%d"), round(open_, 2),
                     round(high, 2), round(low, 2), round(price, 2), volume))
    return rows

def load_data():
    conn = get_connection()
    cursor = conn.cursor()
    for co in COMPANIES:
        cursor.execute("""
            INSERT OR IGNORE INTO companies (ticker, name, sector, industry)
            VALUES (?, ?, ?, ?)
        """, (co["ticker"], co["name"], co["sector"], co["industry"]))
        conn.commit()
        cursor.execute("SELECT id FROM companies WHERE ticker=?", (co["ticker"],))
        company_id = cursor.fetchone()[0]
        prices = simulate_prices(co["ticker"])
        cursor.executemany("""
            INSERT OR IGNORE INTO daily_prices (company_id, date, open, high, low, close, volume)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [(company_id, *row) for row in prices])
        for row in FINANCIALS[co["ticker"]]:
            cursor.execute("""
                INSERT OR IGNORE INTO financials
                (company_id, year, revenue, gross_profit, net_income, total_assets, total_liabilities, equity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (company_id, *row))
        print(f"  ✅ Loaded {co['ticker']} — {len(prices)} price records + {len(FINANCIALS[co['ticker']])} financial years")
    conn.commit()
    conn.close()
    print("\n✅ All data loaded into database.")

if __name__ == "__main__":
    load_data()
