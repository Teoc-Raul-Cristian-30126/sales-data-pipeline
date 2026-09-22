import csv
import random
from datetime import date, timedelta
from pathlib import Path


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

RANDOM_SEED = 42
NUM_PRODUCTS = 100
NUM_STORES = 10
NUM_SALES = 50_000

random.seed(RANDOM_SEED)

# -----------------------------
# Sample data
# -----------------------------

CATEGORIES = [
    "Electronics",
    "Food",
    "Beverages",
    "Clothing",
    "Home",
    "Sports",
    "Beauty",
    "Books",
]

CITIES = [
    "Cluj-Napoca",
    "Bistrita",
    "Baia Mare",
    "Oradea",
    "Sibiu",
    "Brasov",
    "Timisoara",
    "Iasi",
    "Bucharest",
    "Arad",
]

# -----------------------------
# Generate products
# -----------------------------

def generate_products():
    products = []

    for product_id in range(1, NUM_PRODUCTS + 1):
        category = random.choice(CATEGORIES)

        product = {
            "product_id": product_id,
            "product_name": f"{category} Product {product_id}",
            "category": category,
        }

        products.append(product)

    return products

# -----------------------------
# Generate stores
# -----------------------------

def generate_stores():
    stores = []

    for store_id in range(1, NUM_STORES + 1):
        city = CITIES[store_id - 1]

        store = {
            "store_id": store_id,
            "store_name": f"Store {store_id}",
            "city": city,
        }

        stores.append(store)

    return stores

# -----------------------------
# Generate sales
# -----------------------------

def generate_sales():
    sales = []

    start_date = date(2025, 1, 1)
    end_date = date(2025, 12, 31)

    date_range = (end_date - start_date).days

    for sale_id in range(1, NUM_SALES + 1):
        sale_date = start_date + timedelta(
            days=random.randint(0, date_range)
        )

        product_id = random.randint(1, NUM_PRODUCTS)
        store_id = random.randint(1, NUM_STORES)

        quantity = random.randint(1, 5)

        unit_price = round(
            random.uniform(5.0, 500.0),
            2
        )

        sale = {
            "sale_id": sale_id,
            "product_id": product_id,
            "store_id": store_id,
            "sale_date": sale_date.isoformat(),
            "quantity": quantity,
            "unit_price": unit_price,
        }

        sales.append(sale)

    return sales

# -----------------------------
# Write CSV
# -----------------------------

def write_csv(file_path, rows, fieldnames):
    with open(
        file_path,
        mode="w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(rows)

# -----------------------------
# Main
# -----------------------------

def main():
    RAW_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("Generating products...")
    products = generate_products()

    print("Generating stores...")
    stores = generate_stores()

    print("Generating sales...")
    sales = generate_sales()

    write_csv(
        RAW_DATA_DIR / "products.csv",
        products,
        [
            "product_id",
            "product_name",
            "category",
        ],
    )

    write_csv(
        RAW_DATA_DIR / "stores.csv",
        stores,
        [
            "store_id",
            "store_name",
            "city",
        ],
    )

    write_csv(
        RAW_DATA_DIR / "sales.csv",
        sales,
        [
            "sale_id",
            "product_id",
            "store_id",
            "sale_date",
            "quantity",
            "unit_price",
        ],
    )

    print()
    print("Dataset generated successfully!")
    print(f"Products: {len(products):,}")
    print(f"Stores:   {len(stores):,}")
    print(f"Sales:    {len(sales):,}")
    print(f"Location: {RAW_DATA_DIR}")

if __name__ == "__main__":
    main()