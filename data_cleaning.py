import pandas as pd
import os


INPUT_FILE = "data/financials_tidy.csv"
OUTPUT_DIR = "data"
YEARS_TO_KEEP = [2022, 2023, 2024, 2025]


METRIC_PRIORITY = {
        "revenue": ["Total Revenue"],
        "cost_of_revenue": ["Cost Of Revenue"],
        "gross_profit": ["Gross Profit"],
        "operating_income": ["Operating Income", "EBIT"],  # prefer Operating Income
        "net_income": ["Net Income", "Net Income Common Stockholders"],
        "interest_expense": ["Interest Expense"],
        "cash": ["Cash And Cash Equivalents", "Cash Cash Equivalents And Short Term Investments"],
        "current_liabilities": ["Current Liabilities"],
        "receivables": ["Accounts Receivable", "Receivables"],
        "inventory": ["Inventory"],
        "total_assets": ["Total Assets"],
        "total_equity": ["Total Equity Gross Minority Interest"],
        "payables": ["Accounts Payable", "Payables"],
        "total_debt": ["Total Debt"],
        "equity": ["Stockholders Equity", "Common Stock Equity"],
        "total_liabilities": ["Total Liabilities Net Minority Interest"],
        "operating_cash_flow": ["Operating Cash Flow", "Cash Flow From Continuing Operating Activities"],
        "capex": ["Capital Expenditure"],
        "free_cash_flow": ["Free Cash Flow"],
    }

def main():
    df=pd.read_csv(INPUT_FILE)
    print(f"Loaded {len(df)} rows from {INPUT_FILE}")

    # 1. Filter to years we're comparing 
    df=df[df["year"].isin(YEARS_TO_KEEP)]
    print(f"After filtering to years {YEARS_TO_KEEP}: {len(df)} rows")

    rows = []
    for (company, year), group in df.groupby(["company", "year"]):
        available = dict(zip(group["line_item"], group["value"]))
        for metric, candidates in METRIC_PRIORITY.items():
            for name in candidates:
                if name in available:
                    rows.append({
                        "company": company, "year": year, "metric": metric,
                        "value": available[name], "source_line_item": name,
                    })
                    break  # stop at first match — don't add the alternate too
    df = pd.DataFrame(rows)
    print(f"After filtering to needed line items: {len(df)} rows")
    
    #force numeric dtype
    df["value"]= pd.to_numeric(df["value"],errors="coerce")
    n_bad= df["value"].isna().sum()
    if n_bad:
        print(f"\nWARNING: {n_bad} rows had non-numeric values and became NaN after conversion.")
    df = df.dropna(subset=["value"])

    # Check for duplicate rows 
    dup_cols=["company", "year", "metric"]
    n_dupes=df.duplicated(subset=dup_cols).sum()
    print(f"\nDuplicate rows on {dup_cols}: {n_dupes}")
    if n_dupes:
        print("Dropping duplicates, keeping first occurrence.")
        df = df.drop_duplicates(subset=dup_cols, keep="first")

    mask = (df["company"] == "puma") & (df["year"] == 2024) & (df["metric"] == "revenue")
    df.loc[mask, "value"] = 8817200000
    df.loc[mask, "source_line_item"] = "MANUAL OVERRIDE (PUMA AR2024, audited)"

    clean = df[["company", "year", "metric", "value","source_line_item"]].sort_values(
        ["company", "year", "metric"]
    )

    out_path = f"{OUTPUT_DIR}/financials_clean.csv"
    clean.to_csv(out_path, index=False)
    print(f"\nSaved cleaned data to {out_path} ({len(clean)} rows)")

    # 6. Quick sanity check: show what metrics we have per company/year,
    # so yo  u can see at a glance if anything important is missing.
    coverage = clean.pivot_table(
        index="metric", columns=["company", "year"], values="value", aggfunc="count"
    )
    print("\nCoverage check (count of values found per company/year):")
    print(coverage.fillna(0).astype(int))


if __name__ == "__main__":
    main()

















