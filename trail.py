con.sql("""
WITH pivoted AS (
    SELECT
        company,
        year,
        MAX(CASE WHEN metric = 'revenue'         THEN value END) AS revenue,
        MAX(CASE WHEN metric = 'cost_of_revenue' THEN value END) AS cost_of_revenue,
        MAX(CASE WHEN metric = 'receivables'     THEN value END) AS receivables,
        MAX(CASE WHEN metric = 'inventory'       THEN value END) AS inventory,
        MAX(CASE WHEN metric = 'payables'        THEN value END) AS payables
    FROM financials
    GROUP BY company, year
),
days AS (
    SELECT
        company,
        year,
        receivables / revenue * 365         AS dso,
        inventory / cost_of_revenue * 365   AS dio,
        payables / cost_of_revenue * 365    AS dpo
    FROM pivoted
)
SELECT
    company,
    year,
    ROUND(dso, 1)             AS dso_days,
    ROUND(dio, 1)             AS dio_days,
    ROUND(dpo, 1)             AS dpo_days,
    ROUND(dso + dio - dpo, 1) AS cash_conversion_cycle_days
FROM days
ORDER BY company, year
""").df()