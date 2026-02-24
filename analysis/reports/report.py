import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from analysis.queries import (
    get_moving_averages, get_financial_ratios,
    get_volatility_summary, detect_anomalies
)

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "reports")
TICKERS = ["AAPL", "MSFT", "TSLA", "AMZN", "GOOGL"]

BG     = "#0d1117"
CARD   = "#161b22"
BORDER = "#30363d"
TEXT   = "#e6edf3"
MUTED  = "#8b949e"
COLORS = ["#58a6ff", "#3fb950", "#f78166", "#d2a8ff", "#ffa657"]

def _style_ax(ax, title=""):
    ax.set_facecolor(CARD)
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor(BORDER)
    if title:
        ax.set_title(title, color=TEXT, fontsize=10, fontweight="bold", pad=8)
    ax.xaxis.label.set_color(MUTED)
    ax.yaxis.label.set_color(MUTED)

def chart_price_and_ma(ticker):
    df = get_moving_averages(ticker)
    fig = plt.figure(figsize=(14, 7), facecolor=BG)
    gs  = gridspec.GridSpec(2, 1, height_ratios=[3, 1], hspace=0.05)
    ax1 = fig.add_subplot(gs[0])
    ax1.plot(df["date"], df["close"], color="#58a6ff", linewidth=1.2, label="Close")
    ax1.plot(df["date"], df["MA50"],  color="#ffa657", linewidth=1, linestyle="--", label="MA 50")
    ax1.plot(df["date"], df["MA200"], color="#f78166", linewidth=1, linestyle="--", label="MA 200")
    ax1.fill_between(df["date"], df["close"], alpha=0.05, color="#58a6ff")
    _style_ax(ax1, f"{ticker} — Price & Moving Averages")
    ax1.set_xticklabels([])
    ax1.legend(facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT, fontsize=8)
    ax1.set_ylabel("Price (USD)")
    ax2 = fig.add_subplot(gs[1])
    ax2.bar(df["date"], df["volume"] / 1e6, color="#30363d", width=1)
    _style_ax(ax2)
    ax2.set_ylabel("Volume (M)", fontsize=8)
    ax2.set_xlabel("Date")
    fig.patch.set_facecolor(BG)
    path = os.path.join(OUTPUT_DIR, f"{ticker}_price_ma.png")
    plt.savefig(path, dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print(f"  📊 Saved: {ticker}_price_ma.png")

def chart_financial_ratios():
    df = get_financial_ratios()
    latest = df.groupby("ticker").last().reset_index()
    metrics = [
        ("gross_margin_pct", "Gross Margin %"),
        ("net_margin_pct",   "Net Margin %"),
        ("roa_pct",          "Return on Assets %"),
        ("roe_pct",          "Return on Equity %"),
        ("leverage_ratio",   "Leverage Ratio (x)"),
    ]
    fig, axes = plt.subplots(1, len(metrics), figsize=(16, 5), facecolor=BG)
    for ax, (col, title) in zip(axes, metrics):
        vals   = latest[col].values
        labels = latest["ticker"].values
        bars = ax.barh(labels, vals, color=COLORS[:len(labels)], edgecolor=BORDER, height=0.6)
        for bar, val in zip(bars, vals):
            ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height() / 2,
                    f"{val:.1f}", va="center", color=TEXT, fontsize=8)
        _style_ax(ax, title)
        ax.invert_yaxis()
    fig.suptitle("Financial Ratio Comparison — Latest Year", color=TEXT, fontsize=13, fontweight="bold", y=1.02)
    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "ratio_comparison.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  📊 Saved: ratio_comparison.png")

def chart_margin_trends():
    df = get_financial_ratios()
    fig, axes = plt.subplots(1, 2, figsize=(14, 5), facecolor=BG)
    for ax, (col, title) in zip(axes, [
        ("gross_margin_pct", "Gross Margin % Over Time"),
        ("net_margin_pct",   "Net Margin % Over Time"),
    ]):
        for i, ticker in enumerate(TICKERS):
            sub = df[df["ticker"] == ticker]
            ax.plot(sub["year"], sub[col], marker="o", color=COLORS[i], linewidth=2, markersize=5, label=ticker)
        _style_ax(ax, title)
        ax.set_xlabel("Year")
        ax.set_ylabel("%")
        ax.legend(facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT, fontsize=8)
        ax.grid(axis="y", color=BORDER, linestyle="--", alpha=0.5)
    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "margin_trends.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  📊 Saved: margin_trends.png")

def chart_revenue_growth():
    df = get_financial_ratios()
    fig, ax = plt.subplots(figsize=(12, 5), facecolor=BG)
    years   = sorted(df["year"].unique())
    bottoms = [0] * len(years)
    for i, ticker in enumerate(TICKERS):
        sub  = df[df["ticker"] == ticker].set_index("year")
        vals = [sub.loc[y, "revenue"] / 1e3 if y in sub.index else 0 for y in years]
        ax.bar(years, vals, bottom=bottoms, color=COLORS[i], label=ticker, edgecolor=BG, linewidth=0.5)
        bottoms = [b + v for b, v in zip(bottoms, vals)]
    _style_ax(ax, "Total Revenue by Company (USD Billions)")
    ax.set_xlabel("Year")
    ax.set_ylabel("Revenue (USD B)")
    ax.legend(facecolor=CARD, edgecolor=BORDER, labelcolor=TEXT, fontsize=9)
    ax.grid(axis="y", color=BORDER, linestyle="--", alpha=0.4)
    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "revenue_growth.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  📊 Saved: revenue_growth.png")

def chart_anomaly_summary():
    flags = detect_anomalies()
    fig, ax = plt.subplots(figsize=(11, max(3, len(flags) * 0.45 + 1.5)), facecolor=BG)
    ax.set_facecolor(BG)
    ax.axis("off")
    if flags.empty:
        ax.text(0.5, 0.5, "✅ No anomalies detected", ha="center", va="center",
                color="#3fb950", fontsize=14, transform=ax.transAxes)
    else:
        colors_map = {"WARNING": "#ffa657", "DANGER": "#f78166"}
        rows = flags[["ticker", "year", "severity", "flag"]].values.tolist()
        table = ax.table(cellText=rows, colLabels=["Ticker","Year","Severity","Flag"],
                         cellLoc="center", loc="center", bbox=[0, 0, 1, 1])
        table.auto_set_font_size(False)
        table.set_fontsize(9)
        for (r, c), cell in table.get_celld().items():
            cell.set_facecolor(CARD if r > 0 else "#21262d")
            cell.set_edgecolor(BORDER)
            if r == 0:
                cell.set_text_props(color=TEXT, fontweight="bold")
            elif c == 2:
                cell.set_text_props(color=colors_map.get(rows[r-1][2], TEXT), fontweight="bold")
            else:
                cell.set_text_props(color=TEXT)
    ax.set_title("Audit Anomaly Flags", color=TEXT, fontsize=12, fontweight="bold", pad=12)
    fig.patch.set_facecolor(BG)
    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, "anomaly_flags.png"), dpi=130, bbox_inches="tight", facecolor=BG)
    plt.close()
    print("  📊 Saved: anomaly_flags.png")

def generate_all_reports():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("\n📈 Generating charts...")
    for ticker in TICKERS:
        chart_price_and_ma(ticker)
    chart_financial_ratios()
    chart_margin_trends()
    chart_revenue_growth()
    chart_anomaly_summary()
    print(f"\n✅ All charts saved to reports/")

if __name__ == "__main__":
    generate_all_reports()
