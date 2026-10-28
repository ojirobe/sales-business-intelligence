-- PROJECT 1: GEOGRAPHICAL SALES ANALYSIS
-- Business question:
-- Which countries generate the highest merchandise sales?

SELECT
    Country,

    COUNT(*) AS TransactionLines,

    COUNT(DISTINCT InvoiceNo) AS InvoiceCount,

    ROUND(
        SUM(TRY_CAST(Revenue AS DOUBLE)), 2
    ) AS GrossMerchandiseValue

FROM read_csv_auto(
    'data/processed/classified_sales.csv',
    all_varchar = true
)

WHERE TransactionCategory = 'Merchandise'
  AND Country IS NOT NULL
  AND TRIM(Country) <> ''

GROUP BY Country

ORDER BY GrossMerchandiseValue DESC;