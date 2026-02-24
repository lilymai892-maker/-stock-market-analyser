import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "stock_data.db")

def get_connection():
    return sqlite3.connect(DB_PATH)

def create_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ticker TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            sector TEXT,
            industry TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS daily_prices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume INTEGER,
            FOREIGN KEY (company_id) REFERENCES companies(id),
            UNIQUE(company_id, date)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS financials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL,
            year INTEGER NOT NULL,
            revenue REAL,
            gross_profit REAL,
            net_income REAL,
            total_assets REAL,
            total_liabilities REAL,
            equity REAL,
            FOREIGN KEY (company_id) REFERENCES companies(id),
            UNIQUE(company_id, year)
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database created successfully.")

if __name__ == "__main__":
    create_database()
