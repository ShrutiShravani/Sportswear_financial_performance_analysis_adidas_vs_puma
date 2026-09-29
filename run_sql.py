"""
Run a .sql file against the cleaned financials using DuckDB.

Usage (from the project folder):
    python run_sql.py sql/01_revenue_growth.sql

The cleaned CSV is exposed as a table called `financials` with columns:
    company, year, metric, value, source_line_item
(one row per company / year / metric, so ratios need a pivot or self-join)
"""

import sys
import duckdb

CSV_PATH = "data/financials_clean.csv"


def main():
    if len(sys.argv) < 2:
        print("Usage: python run_sql.py path/to/query.sql")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        query = f.read()

    con = duckdb.connect()
    con.execute(
        f"CREATE VIEW financials AS SELECT * FROM read_csv_auto('{CSV_PATH}')"
    )
    # One query per file. Show everything, not a truncated preview.
    print(con.sql(query).df().to_string(index=False))


if __name__ == "__main__":
    main()