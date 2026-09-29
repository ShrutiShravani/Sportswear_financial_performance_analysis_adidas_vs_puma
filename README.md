# European Sportswear Financial Performance Analysis: adidas vs Puma

A full-cycle financial analytics project — from data extraction to interactive
dashboard — comparing adidas and Puma's financial performance from 2022 to 2025.
Built as a portfolio project for Financial Analyst / FP&A / Data Analyst roles.

## Project Summary

This project analyzes the historical financial statements of two competing
European sportswear companies to answer one central question: **how healthy
and well-run are adidas and Puma, and does their profit turn into cash?**

Rather than just calculating ratios, every significant finding in this project
is investigated and explained using the companies' own annual reports and
press releases — connecting *what* the numbers show to *why* they moved.

**The headline story:** adidas recovered from a 2023 dip (driven by the end of
the Yeezy partnership) through pricing discipline and cost control, reaching
record revenue and its strongest margins in this period by 2025. Puma, after
several stable years, undertook a deliberate strategic reset in 2025 — cutting
wholesale volume and clearing inventory — which drove a 13% revenue decline,
a negative operating margin, and a sharp rise in leverage.

## Tech Stack

| Tool | Role in this project |
|---|---|
| **Python** (pandas, yfinance) | Data extraction from public financial statements, cleaning, and transformation |
| **SQL** (DuckDB) | All ratio calculations and comparative/analytical queries |
| **Power BI** | Interactive 3-page dashboard (KPI overview, performance trends, cash & working capital) |
| **Excel** | Assumption-driven forecast model *(in progress)* |

## Data Sources

- **Financial statements:** pulled via the `yfinance` Python library (income
  statement, balance sheet, cash flow), sourced originally from each company's
  audited annual reports. Covers FY2022–FY2025.
- **One data correction:** yfinance returned an incorrect FY2024 revenue figure
  for Puma (€8,398.0m). This was cross-checked against Puma's audited FY2024
  annual report (€8,817.2m) and corrected via a documented manual override in
  `clean_financials.py`.
- **Qualitative context:** drivers behind financial movements (margin changes,
  inventory decisions, leverage changes) are sourced directly from adidas's and
  Puma's own annual reports, earnings press releases, and investor
  presentations. Every claim of "why" something changed is cited; where no
  source was found, this is explicitly noted rather than inferred.

## Project Structure

```
├── fetch_financials.py          # Pulls raw financial statements via yfinance
├── clean_financials.py          # Cleans, standardizes, and validates the data
├── financial_data/
│   ├── financials_tidy.csv      # Raw extracted data (long format)
│   ├── financials_clean.csv     # Cleaned, deduplicated, analysis-ready data
│   └── financials.xlsx          # Wide-format Excel version
├── analysis.ipynb                # DuckDB SQL analysis (all ratios + queries)
├── dashboard/
│   ├── adidas_puma_dashboard.pbix
│   └── screenshots/              # PDF/PNG exports of dashboard pages
└── README.md
```

## Methodology

1. **Extraction:** 4 years of income statement, balance sheet, and cash flow
   data pulled for both companies via yfinance.
2. **Cleaning:** ~150 raw line items per statement filtered down to 16 core
   metrics needed for analysis, using a priority-list mapping to avoid
   duplicate or conflicting values (e.g., choosing "Operating Income" over the
   similar but distinct "EBIT" line, consistently).
3. **Data integrity check:** confirmed Assets = Liabilities + Equity for both
   companies, all 4 years (difference = €0 in every case).
4. **Ratio analysis (SQL):** revenue growth, gross/EBIT/net margin, ROCE,
   debt-to-equity, interest coverage, DSO/DIO/DPO/cash conversion cycle,
   operating cash flow vs. net income.
5. **Root-cause investigation:** for every significant ratio movement, the
   underlying driver was researched and sourced from primary company
   documents (see Key Findings below).
6. **Naive budget-vs-actual test:** built a simple trend-based revenue
   forecast (prior year × historical average growth) for 2024 and 2025, to
   test whether a naive model would have anticipated each company's actual
   performance.
7. **Dashboard:** 3-page interactive Power BI report.

## Key Findings

### Profitability
adidas's gross margin rose from 47.3% (2022) to 51.6% (2025), driven by
pricing discipline and lower freight/product costs — despite currency
headwinds and tariffs. Puma's gross margin fell from 47.6% (2024) to 44.9%
(2025) due to elevated wholesale promotions and inventory write-downs tied to
its distribution reset.

### Capital Efficiency (ROCE)
adidas's ROCE rose from 6.6% (2022) to 18.5% (2025), driven almost entirely by
margin recovery rather than more efficient capital use — capital employed
actually grew (World Cup 2026 inventory build) but margin gains outweighed it.
Puma's ROCE fell from 16.3% to -11.0% over the same period, tracking its
margin collapse.

### Cash Conversion Cycle
Both companies saw their cash conversion cycle lengthen in 2025, but for
opposite reasons: adidas's reflects a deliberate inventory investment ahead of
anticipated 2026 demand; Puma's reflects the mechanical effect of a shrinking
revenue base outpacing falling receivables and payables.

### Leverage
adidas deleveraged steadily (debt-to-equity 1.29 → 0.96), ending 2025 strong
enough to announce a €1 billion share buyback. Puma's leverage nearly doubled
(0.61 → 1.47) as new debt (promissory notes, a bridge loan) funded its
turnaround while equity shrank from the reported loss.

### Naive Forecast Test
A simple trend-based model would have closely predicted adidas's 2025 revenue
(within +1.9%), but would have overestimated Puma's 2025 revenue by roughly
19% — confirming that Puma's decline was a deliberate strategic choice, not
organic drift a trend model could anticipate.

## Limitations

- Some individual working-capital movements (specific DSO/DPO changes in
  certain years) are visible in the data but not explained at that level of
  detail in the sources reviewed. These are explicitly marked as "not
  disclosed" rather than guessed.
- ROCE uses year-end (not average) capital employed, a common simplification.
- The "naive budget" in this project is a simplified analytical exercise
  (prior year × historical growth), not either company's actual internal
  budget, which is not public.
- Financial data reflects yfinance's extraction of public statements; one
  known data error was found and corrected (see Data Sources).

## Author's Note

This project was built to demonstrate an end-to-end financial analysis
workflow: extracting and cleaning real data, calculating and interpreting
financial ratios, connecting quantitative findings to sourced qualitative
explanations, and communicating results through an interactive dashboard —
skills directly relevant to Financial Analyst, FP&A, and Data Analyst roles.
