-- PRODUCT PERFORMANCE ANALYSIS
-- Identify the top 10 products by positive merchandise value

SELECT
    StockCode,
    Description,

    SUM(TRY_CAST(Quantity AS BIGINT)) AS UnitsSold,

    COUNT(DISTINCT InvoiceNo) AS InvoiceCount,

    ROUND(
        SUM(TRY_CAST(Revenue AS DOUBLE)), 2
    ) AS GrossSalesValue

FROM read_csv_auto(
    'data/processed/classified_sales.csv',
    all_varchar = true
)

WHERE TransactionCategory = 'Merchandise'
  AND Description IS NOT NULL
  AND TRIM(Description) <> ''

GROUP BY StockCode, Description

ORDER BY GrossSalesValue DESC

LIMIT 10;