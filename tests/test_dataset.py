import pandas as pd


def test_products_dataset():
    df = pd.read_csv("data/raw/products.csv")

    assert len(df) == 100
    assert df["product_id"].is_unique
    assert df["product_name"].notna().all()
    assert df["category"].notna().all()


def test_stores_dataset():
    df = pd.read_csv("data/raw/stores.csv")

    assert len(df) == 10
    assert df["store_id"].is_unique
    assert df["store_name"].notna().all()
    assert df["city"].notna().all()


def test_sales_dataset():
    df = pd.read_csv("data/raw/sales.csv")

    assert len(df) == 50_000
    assert df["sale_id"].is_unique
    assert df["product_id"].notna().all()
    assert df["store_id"].notna().all()
    assert df["sale_date"].notna().all()
    assert df["quantity"].gt(0).all()
    assert df["unit_price"].gt(0).all()