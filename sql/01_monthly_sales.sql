
-- PROJECT 1: SALES & BUSINESS INTELLIGENCE
-- BUSINESS QUESTION:
-- What is the monthly positive merchandise sales value?

SELECT
    strftime(
        TRY_CAST(InvoiceDate AS TIMESTAMP),
        '%Y-%m'
    ) AS SalesMonth,

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

GROUP BY SalesMonth
ORDER BY SalesMonth;