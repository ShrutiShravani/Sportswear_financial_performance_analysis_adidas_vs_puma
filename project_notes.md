
## Project
**European Sportswear Financial Performance Analysis: adidas vs Puma**
Central question: how healthy and well-run are adidas and Puma, and does profit turn into cash?

## Data
- Source: yfinance, tickers ADS.DE (adidas) and PUM.DE (Puma, NOT PUMA.DE)
- adidas: 2022-2025. Puma: 2021-2025 but 2021 mostly empty, so both trimmed to 2022-2025
- Statements are IFRS annual figures. Not verified against annual reports yet
- Files:
  - fetch_financials.py -> financial_data/financials_tidy.csv (+ raw CSVs, financials.xlsx)
  - clean_financials.py -> financial_data/financials_clean.csv
    columns: company, year, metric, value, source_line_item
- Cleaning uses a priority list per metric (e.g. Operating Income before EBIT) so each
  company/year/metric has exactly one value. adidas reports both Net Income and
  Net Income Common Stockholders; EBIT (2048m) differs from Operating Income (2061m) for 2025.
- Metrics kept: revenue, cost_of_revenue, gross_profit, operating_income, net_income,
  interest_expense, cash, receivables, inventory, total_assets, payables, total_debt,
  equity, total_liabilities, operating_cash_flow, capex, free_cash_flow
- TODO: add Current Liabilities to the mapping (needed for ROCE), then re-run cleaning
- TODO: confirm the coverage table from clean_financials.py shows no gaps

## adidas figures seen so far (from yfinance income statement)
- Revenue: 2022 22,511m | 2023 21,427m | 2024 23,683m | 2025 24,811m
- Net income: 2022 612m | 2023 -75m | 2024 764m | 2025 1,340m
- Hypothesis to test: what drove the 2023 dip and the strong recovery?

## Analysis questions (ratios exist to answer these)
1. Is the business growing? -> revenue growth %
2. Is it profitable, and where does profit leak? -> gross, EBIT, net margin
3. Does profit become cash? -> DSO, DIO, DPO, cash conversion cycle, operating cash flow vs net income
4. Is it financially safe? -> debt-to-equity, interest coverage
5. Does it use capital well? -> ROCE
Balance check (assets = liabilities + equity) is a data quality check, not analysis.

## Decisions made
- All ratio calculation and comparison analysis done in SQL (DuckDB) first
- Python/Pandas redo is optional, for practice, after the project is done
- Excel is kept: it is where the forward-looking forecast model is built
- No cloud/AWS. Credit risk project dropped from this project
- Statements are analyzed, not created. Only the forecast is built by us
- Company data is real (public); the budget in the variance step is a naive backtest
  (prior year x historical growth), labeled as such in the README

## Plan order
1. SQL ratios + comparison queries (run with run_sql.py)
2. The "why" behind two ratios (margin change, profit vs cash gap)
3. adidas vs Puma conclusion
4. Naive budget vs actual variance
5. Power BI dashboard
6. Excel forecast (base case, scenarios later)
7. README / case study
8. Optional: Python redo for practice

## Interview prep (after the project)
Question banks already discussed: Power BI (30), statistics (54), Python/Pandas (57),
finance cases, product-case framework. Practice files: orders.csv, customers.csv.


adidas — DSO, DIO, DPO, CCC
2022 → 2023 (CCC 135.3 → 105.5, DIO 183.7 → 146.9 days): adidas deliberately cut inventory. The 2023 annual report states plainly that decisive actions significantly reduced inventory levels through limiting sell-in to the wholesale channel. Source: Annual Report 2023
2023 → 2024 (CCC 105.5 → 96.5, DPO 73.9 → 96.9 days): average operating working capital as % of net sales fell from 25.7% to 19.7%, adidas's best working capital efficiency in this period, alongside strong sales growth. I don't have a specific line explaining the DPO rise (paying suppliers slower), so treat that one part as unconfirmed; it's plausible it reflects normal negotiation or timing, not sourced.
2024 → 2025 (CCC 96.5 → 127.6, DIO 156.2 → 177.3, DSO 37.2 → 38.8): this reverses the improvement. adidas's 2025 annual report is explicit: inventories increased 17% to €5,832m, reflecting the company's planned top-line growth as well as earlier product purchases related to the FIFA World Cup 2026 and faster inbound deliveries. Operating working capital rose 29% to €5,556m. Receivables rose 9.2% to €2,634m, roughly matching revenue growth. Source: Annual Report 2025 — Statement of Financial Position
Puma — DSO, DIO, DPO, CCC
2022 (DIO 179.4 days, high): Puma's own factsheet shows inventories up 50% year-on-year at end-2022, split into on-hand stock (+84%) and in-transit (+8%). This was widely reported industry-wide overstocking risk after supply chain disruption. Source: PUMA Q4 2022 factsheet
2022 → 2023 (CCC 86.5 → 71.3, DIO 179.4 → 142.5 days): Puma's 2023 factsheet confirms inventories fell 20% year-on-year and trade payables fell 14%, working capital improved. This lines up with your DIO drop. Source: PUMA FY2023 factsheet
2023 → 2024 (CCC 71.3 → 64.1, DPO 118.6 → 157.1 days): Puma's 2024 consolidated statements confirm trade payables rose sharply, from €1,499.8m to €1,893.5m, which lines up with your DPO jump (paying suppliers slower, or negotiating longer terms). Source: PUMA AR2024 consolidated financial statements
2024 → 2025 (CCC 64.1 → 117.2, big jump, DIO 167.0 → 187.1): ties directly to the 2025 reset story you already have: inventory reserves from distribution clean-up and elevated stock levels being deliberately worked down. Same source as your profitability "why" above