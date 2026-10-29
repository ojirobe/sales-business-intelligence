# Retail Sales Intelligence Dashboard

### An Interactive Business Intelligence and Customer Analytics Portfolio Project

An end-to-end retail analytics project using Python, Pandas, SQL, DuckDB, Plotly and Streamlit to investigate historical retail transactions, evaluate product performance, segment customers and examine international sales patterns.

## Project Overview

This project analyses the **UCI Online Retail Dataset**, containing 541,909 transaction records from December 2010 to December 2011.

The objective is to transform raw transactional data into meaningful business intelligence through systematic data preparation, exploratory analysis, SQL aggregation, customer segmentation and interactive visualisation.

**Dataset:** [UCI Online Retail](https://archive.ics.uci.edu/dataset/352/online+retail)

## Business Questions

1. How did merchandise sales change across the reporting period?
2. Which products generated the highest gross and net transaction values?
3. How did cancellations and returns affect product rankings?
4. How can customers be grouped using Recency, Frequency and Monetary (RFM) analysis?
5. Which international markets contributed most to positive merchandise sales?
6. How can data quality checks improve confidence in analytical results?

## Key Findings

| Indicator | Result |
|---|---:|
| Original dataset | 541,909 rows |
| Classified transaction dataset | 530,104 rows |
| Positive merchandise transaction lines | 527,713 |
| Positive merchandise sales | £10,270,918.87 |
| Unique sales invoices | 19,773 |
| Identifiable customers in RFM segmentation | 4,333 |
| UK share of positive merchandise sales | 85.16% |
| Parquet storage reduction | 94.85% |
| Automated integrity tests | 6 passed |

*Positive merchandise sales are calculated before returns and cancellations. They should not be interpreted as net revenue or profit.*

## Interactive Dashboard

The application contains six navigable sections.

**Home:** Project introduction, summary indicators and analytical navigation.

**Sales Overview:** Monthly sales trends, invoice-level KPIs and country filters.

**Product Performance:** Product rankings by gross sales, net sales and net units.

**Customer Analytics:** RFM segmentation, customer distribution and purchasing behaviour.

**Geographical Analytics:** UK sales concentration and international market rankings.

**Methodology:** Data quality assessment, KPI definitions, reconciliation checks and analytical limitations.

## Technology Stack

- Python and Pandas for data processing and analysis
- DuckDB and SQL for analytical querying
- PyArrow and Parquet for efficient data storage
- Plotly for interactive visualisations
- Streamlit for the multipage dashboard
- Pytest for automated data integrity testing
- Git and GitHub for version control

## Data Preparation and Validation

The analysis investigates missing customer identifiers, missing product descriptions, exact duplicate records, negative quantities, cancellation invoices, unusual stock codes and non-merchandise transaction categories.

Transaction classifications were developed to separate merchandise sales from shipping charges, marketplace fees, accounting adjustments and other records.

Exact duplicates were assessed through a sensitivity analysis rather than automatically removed without review.

The original 69.10 MB classified CSV dataset was converted to a 3.56 MB Parquet file, achieving a 94.85% storage reduction. The conversion was validated through row-count and DataFrame comparisons.

## Customer Segmentation

Customer segmentation uses three RFM measures.

**Recency:** Days since the customer's most recent qualifying retained purchase.

**Frequency:** Number of qualifying purchase invoices.

**Monetary:** Signed transaction value attributed to the customer.

The preliminary segmentation identifies 909 Champions, 2,006 Regular Customers, 965 Hibernating Customers, 238 New or Occasional Customers, 206 At Risk Customers and 9 customers requiring further review.

These classifications remain provisional because some cancellation matches have not been fully resolved.

## Installation and Running the Dashboard

Clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd sales-business-intelligence
```

Create a Python virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install project dependencies:

```bash
python -m pip install -r requirements.txt
```

Launch the dashboard:

```bash
python -m streamlit run app.py
```

Open the local address displayed by Streamlit, usually `http://localhost:8501`.

## Automated Testing

Run the data integrity tests:

```bash
python -m pytest tests/ -v
```

The test suite checks classified transaction counts, merchandise record counts, positive sales totals, geographical reconciliation, RFM customer counts and the Champions segment.

The current six tests pass. These checks do not constitute a complete audit of all transaction classifications.

## Analytical Limitations

The dataset is historical and does not represent current retail performance.

Positive merchandise sales exclude negative transactions.

Some cancellation and return matches remain unresolved.

Customer segmentation results are preliminary.

December 2011 is an incomplete reporting month.

The dataset does not contain sufficient cost information for reliable profit calculations.

## Project Status

The interactive Streamlit application and initial data integrity testing have been completed.

## Author

Yunusa A. Ojirobe

Statistics | Data Analytics | Business Intelligence | Research