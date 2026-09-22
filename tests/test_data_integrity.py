import pandas as pd


def test_sales_product_relationship():
    products = pd.read_csv("data/raw/products.csv")
    sales = pd.read_csv("data/raw/sales.csv")

    product_ids = set(products["product_id"])

    assert sales["product_id"].isin(product_ids).all()


def test_sales_store_relationship():
    stores = pd.read_csv("data/raw/stores.csv")
    sales = pd.read_csv("data/raw/sales.csv")

    store_ids = set(stores["store_id"])

    assert sales["store_id"].isin(store_ids).all()


def test_sales_ids_are_unique():
    sales = pd.read_csv("data/raw/sales.csv")

    assert sales["sale_id"].is_unique


def test_sales_dates_are_valid():
    sales = pd.read_csv("data/raw/sales.csv")

    dates = pd.to_datetime(sales["sale_date"])

    assert dates.min() >= pd.Timestamp("2025-01-01")
    assert dates.max() <= pd.Timestamp("2025-12-31")


def test_total_amount_is_positive():
    sales = pd.read_csv("data/raw/sales.csv")

    total_amount = sales["quantity"] * sales["unit_price"]

    assert (total_amount > 0).all()