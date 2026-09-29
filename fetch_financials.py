import yfinance as yf
import pandas as pd
import os

from pathlib import Path

OUTPUT_DIR = Path(__file__).resolve().parent
os.makedirs(OUTPUT_DIR,exist_ok=True)
 
COMPANIES={
    "adidas":"ADS.DE",
    "puma": "PUM.DE"
}

def fetch_company(name,ticker):
    print(f"Fetching {name} ({ticker})...")
    t=yf.Ticker(ticker)

    income_stmt=t.financials 
    balance_sheet=t.balance_sheet
    cash_flow= t.cashflow

    

    if income_stmt.empty or balance_sheet.empty or cash_flow.empty:
          print(f"  WARNING: one or more statements came back empty for {ticker}. "
              f"Yahoo may be rate-limiting or the ticker/data may be unavailable.")
    
    print(f"  income_stmt shape: {income_stmt.shape}, columns: {list(income_stmt.columns)}")
    print(f"  income_stmt index (first 5): {list(income_stmt.index[:5])}")
    print(f"  income_stmt dtypes:\n{income_stmt.dtypes}")
 
    
    
    income_stmt.to_csv(f"{OUTPUT_DIR}/{name}_income_statement_raw.csv")
    balance_sheet.to_csv(f"{OUTPUT_DIR}/{name}_balance_sheet_raw.csv")
    cash_flow.to_csv(f"{OUTPUT_DIR}/{name}_cash_flow_raw.csv")

    return income_stmt,balance_sheet,cash_flow


def tidy(df,statement_name,company):
    """
    Convert yfinance's wide format (line items as rows, years as columns)
    into a tidy long format: company, statement, line_item, year, value.
    """
    if df.empty or df.shape[1] == 0:
        print(f"  SKIPPING {statement_name} for {company}: no data returned.")
        return pd.DataFrame(columns=["company", "statement", "year", "line_item", "value"])
    df=df.copy()
    df.index.name="line_item"
    stacked = df.stack()
    stacked.name = "value"
    long_df = stacked.reset_index()
    long_df.columns = ["line_item", "year", "value"]
    long_df["year"]=pd.to_datetime(long_df["year"]).dt.year
    long_df["statement"]=statement_name
    long_df["company"]=company

    return long_df[["company","statement","year","line_item","value"]]

def main():
    all_tidy=[]

    for name,ticker in COMPANIES.items():
        income_stmt,balance_sheet,cash_flow= fetch_company(name, ticker)

        all_tidy.append(tidy(income_stmt,"income_statement",name))
        all_tidy.append(tidy(balance_sheet,"balance_sheet",name))
        all_tidy.append(tidy(cash_flow,"cash_flow",name))

    combined =pd.concat(all_tidy,ignore_index=True)
    combined= combined.dropna(subset=["value"]) #drop line items
    #save to csv

    combined.to_csv(OUTPUT_DIR/"financials_tidy.csv",index=False)

    #Also save as excel,one sheet per company
    with pd.ExcelWriter(f"{OUTPUT_DIR}/financials.xlsx") as writer:
        for name in COMPANIES:
            sub=combined[combined["company"]==name]
            wide= sub.pivot_table(index=["statement","line_item"],columns="year",values="value")
            wide.to_excel(writer,sheet_name=name)
    
    print("\n Done")
    print(f"Raw CSVs, tidy CSV, and financials.xlsx are in ./{OUTPUT_DIR}/")
    print(f"Total rows in tidy dataset: {len(combined)}")


if __name__ == "__main__":
    main()







    

