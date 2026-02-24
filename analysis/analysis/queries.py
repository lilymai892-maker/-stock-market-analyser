import pandas as pd
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from database.setup import get_connection

def get_price_history(ticker):
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT dp.date, dp.open, dp.high, dp.low, dp.close, dp.volume
        FROM daily_prices dp
        JOIN companies c ON dp.company_id = c.id
        WHERE c.ticker = ?
        ORDER BY dp.date
    """, conn, params=(ticker,))
    conn.close()
    df["date"] = pd.to_datetime(df["date"])
    return df

def get_financial_ratios():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT
            c.ticker, c.name, c.sector, f.year,
            f.revenue, f.gross_profit, f.net_income,
            f.total_assets, f.total_liabilities, f.equity,
            ROUND(f.gross_profit * 100.0 / f.revenue, 2)      AS gross_margin_pct,
            ROUND(f.net_income  * 100.0 / f.revenue, 2)       AS net_margin_pct,
            ROUND(f.net_income  * 100.0 / f.total_assets, 2)  AS roa_pct,
            ROUND(f.net_income  * 100.0 / f.equity, 2)        AS roe_pct,
            ROUND(f.total_assets * 1.0  / f.equity, 2)        AS leverage_ratio
        FROM financials f
        JOIN companies c ON f.company_id = c.id
        ORDER BY c.ticker, f.year
    """, conn)
    conn.close()
    return df

def get_volatility_summary():
    conn = get_connection()
    df = pd.read_sql_query("""
        SELECT
            c.ticker, c.name,
            COUNT(dp.id)                    AS trading_days,
            ROUND(AVG(dp.close), 2)         AS avg_close,
            ROUND(MIN(dp.close), 2)         AS min_close,
            ROUND(MAX(dp.close), 2)         AS max_close,
            ROUND(AVG(dp.volume) / 1e6, 2)  AS avg_volume_m
        FROM daily_prices dp
        JOIN companies c ON dp.company_id = c.id
        GROUP BY c.ticker
        ORDER BY c.ticker
    """, conn)
    conn.close()
    return df

def get_moving_averages(ticker, short=50, long=200):
    df = get_price_history(ticker)
    df[f"MA{short}"]   = df["close"].rolling(window=short).mean()
    df[f"MA{long}"]    = df["close"].rolling(window=long).mean()
    df["daily_return"] = df["close"].pct_change() * 100
    return df

def detect_anomalies():
    df = get_financial_ratios()
    flags = []
    for ticker, group in df.groupby("ticker"):
        group = group.sort_values("year").reset_index(drop=True)
        for i in range(1, len(group)):
            prev, curr = group.iloc[i - 1], group.iloc[i]
            margin_drop = curr.gross_margin_pct - prev.gross_margin_pct
            if margin_drop < -5:
                flags.append({"ticker": ticker, "year": int(curr.year), "severity": "WARNING",
                               "flag": f"Gross margin dropped {abs(margin_drop):.1f}pp"})
            if curr.leverage_ratio > 4:
                flags.append({"ticker": ticker, "year": int(curr.year), "severity": "DANGER",
                               "flag": f"High leverage ratio: {curr.leverage_ratio:.2f}x"})
            rev_growth = (curr.revenue - prev.revenue) / prev.revenue * 100
            if rev_growth < -5:
                flags.append({"ticker": ticker, "year": int(curr.year), "severity": "WARNING",
                               "flag": f"Revenue declined {abs(rev_growth):.1f}%"})
            if curr.net_income < 0:
                flags.append({"ticker": ticker, "year": int(curr.year), "severity": "DANGER",
                               "flag": f"Net loss recorded: ${curr.net_income:,.0f}M"})
    return pd.DataFrame(flags) if flags else pd.DataFrame(columns=["ticker","year","severity","flag"])
