
from pathlib import Path

import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "processed"


@pytest.fixture(scope="module")
def datasets():
    sales = pd.read_parquet(
        DATA / "classified_sales.parquet"
    )

    geo = pd.read_csv(
        DATA / "geographical_sales.csv"
    )

    rfm = pd.read_csv(
        DATA / "rfm_segments_preliminary.csv"
    )

    sales["Revenue"] = pd.to_numeric(
        sales["Revenue"], errors="coerce"
    )

    sales["InvoiceDate"] = pd.to_datetime(
        sales["InvoiceDate"], errors="coerce"
    )

    merchandise = sales.loc[
        (sales["TransactionCategory"] == "Merchandise")
        & sales["InvoiceDate"].notna()
        & sales["Revenue"].notna()
    ]

    return sales, merchandise, geo, rfm


def test_classified_record_count(datasets):
    sales, _, _, _ = datasets
    assert len(sales) == 530104


def test_merchandise_record_count(datasets):
    _, merchandise, _, _ = datasets
    assert len(merchandise) == 527713


def test_positive_merchandise_sales(datasets):
    _, merchandise, _, _ = datasets

    actual = merchandise["Revenue"].sum()

    assert actual == pytest.approx(
        10270918.87, abs=0.01
    )


def test_geographical_reconciliation(datasets):
    _, merchandise, geo, _ = datasets

    sales_total = merchandise["Revenue"].sum()
    geo_total = geo["GrossMerchandiseValue"].sum()

    assert sales_total == pytest.approx(
        geo_total, abs=0.01
    )


def test_rfm_customer_count(datasets):
    _, _, _, rfm = datasets

    assert len(rfm) == 4333


def test_rfm_champions(datasets):
    _, _, _, rfm = datasets

    champions = (
        rfm["Segment"] == "Champions"
    ).sum()

    assert champions == 909