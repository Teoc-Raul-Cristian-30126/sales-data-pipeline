import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def get_connection():
    return psycopg.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

def load_products(connection):
    file_path = RAW_DATA_DIR / "products.csv"
    df = pd.read_csv(file_path)

    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO products (
                    product_id,
                    product_name,
                    category
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (product_id) DO NOTHING;
                """,
                (
                    row.product_id,
                    row.product_name,
                    row.category,
                ),
            )

    connection.commit()
    print(f"Loaded {len(df):,} products")

def load_stores(connection):
    file_path = RAW_DATA_DIR / "stores.csv"
    df = pd.read_csv(file_path)

    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO stores (
                    store_id,
                    store_name,
                    city
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (store_id) DO NOTHING;
                """,
                (
                    row.store_id,
                    row.store_name,
                    row.city,
                ),
            )

    connection.commit()
    print(f"Loaded {len(df):,} stores")

def load_sales(connection):
    file_path = RAW_DATA_DIR / "sales.csv"
    df = pd.read_csv(file_path)

    with connection.cursor() as cursor:
        for row in df.itertuples(index=False):
            cursor.execute(
                """
                INSERT INTO sales (
                    sale_id,
                    product_id,
                    store_id,
                    sale_date,
                    quantity,
                    unit_price
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (sale_id) DO NOTHING;
                """,
                (
                    row.sale_id,
                    row.product_id,
                    row.store_id,
                    row.sale_date,
                    row.quantity,
                    row.unit_price,
                ),
            )

    connection.commit()
    print(f"Loaded {len(df):,} sales")

def main():
    connection = get_connection()

    try:
        load_products(connection)
        load_stores(connection)
        load_sales(connection)

        print("Data loading completed successfully!")

    finally:
        connection.close()

if __name__ == "__main__":
    main()