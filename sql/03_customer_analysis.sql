-- PROJECT 1: SALES & BUSINESS INTELLIGENCE
-- CUSTOMER BEHAVIOUR ANALYSIS

SELECT
    CustomerID,

    COUNT(DISTINCT InvoiceNo) AS TotalOrders,

    SUM(TRY_CAST(Quantity AS DOUBLE)) AS UnitsPurchased,

    ROUND(
        SUM(TRY_CAST(Revenue AS DOUBLE)), 2
    ) AS GrossPurchaseValue,

    ROUND(
        SUM(TRY_CAST(Revenue AS DOUBLE))
        / NULLIF(COUNT(DISTINCT InvoiceNo), 0),
        2
    ) AS AverageOrderValue

FROM read_csv_auto(
    'data/processed/classified_sales.csv',
    all_varchar = true
)

WHERE TransactionCategory = 'Merchandise'
    AND CustomerID IS NOT NULL
    AND TRIM(CustomerID) <> ''

GROUP BY CustomerID

ORDER BY GrossPurchaseValue DESC;