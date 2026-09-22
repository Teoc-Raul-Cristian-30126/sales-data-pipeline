import os

os.environ["JAVA_HOME"] = r"C:\Users\fery3\.jdks\ms-17.0.20.1"
os.environ["PYSPARK_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"

from dotenv import load_dotenv
load_dotenv()

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum, count, avg


def main():

    spark = (
        SparkSession.builder
        .appName("SalesDataTransformation")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.postgresql:postgresql:42.7.8"
        )
        .getOrCreate()
    )

    jdbc_url = "jdbc:postgresql://localhost:5432/sales_dw"

    connection_properties = {
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "driver": "org.postgresql.Driver"
    }

    print("Reading data from PostgreSQL...")

    sales_df = spark.read.jdbc(
        url=jdbc_url,
        table="sales",
        properties=connection_properties
    )

    products_df = spark.read.jdbc(
        url=jdbc_url,
        table="products",
        properties=connection_properties
    )

    stores_df = spark.read.jdbc(
        url=jdbc_url,
        table="stores",
        properties=connection_properties
    )

    print("Sales:", sales_df.count())
    print("Products:", products_df.count())
    print("Stores:", stores_df.count())

    # --------------------------------------------------
    # 1. Join the three tables
    # --------------------------------------------------

    transformed_df = (
        sales_df
        .join(
            products_df,
            sales_df.product_id == products_df.product_id
        )
        .join(
            stores_df,
            sales_df.store_id == stores_df.store_id
        )
        .select(
            sales_df.sale_id,
            sales_df.sale_date,
            sales_df.product_id,
            products_df.product_name,
            products_df.category,
            sales_df.store_id,
            stores_df.store_name,
            stores_df.city,
            sales_df.quantity,
            sales_df.unit_price
        )
        .withColumn(
            "total_amount",
            col("quantity") * col("unit_price")
        )
        .withColumn(
            "year",
            year("sale_date")
        )
        .withColumn(
            "month",
            month("sale_date")
        )
    )

    print("\nTransformed sales:")
    transformed_df.show(10, truncate=False)

    # --------------------------------------------------
    # 2. Monthly revenue
    # --------------------------------------------------

    monthly_revenue_df = (
        transformed_df
        .groupBy("year", "month")
        .agg(
            sum("total_amount").alias("total_revenue"),
            count("sale_id").alias("number_of_sales"),
            avg("total_amount").alias("average_sale_value")
        )
        .orderBy("year", "month")
    )

    print("\nMonthly revenue:")
    monthly_revenue_df.show(20, truncate=False)

    # --------------------------------------------------
    # 3. Revenue by category
    # --------------------------------------------------

    category_revenue_df = (
        transformed_df
        .groupBy("category")
        .agg(
            sum("total_amount").alias("total_revenue"),
            count("sale_id").alias("number_of_sales")
        )
        .orderBy(col("total_revenue").desc())
    )

    print("\nRevenue by category:")
    category_revenue_df.show(truncate=False)

    # --------------------------------------------------
    # 4. Revenue by store
    # --------------------------------------------------

    store_revenue_df = (
        transformed_df
        .groupBy("store_id", "store_name", "city")
        .agg(
            sum("total_amount").alias("total_revenue"),
            count("sale_id").alias("number_of_sales")
        )
        .orderBy(col("total_revenue").desc())
    )

    print("\nRevenue by store:")
    store_revenue_df.show(truncate=False)

    # --------------------------------------------------
    # 5. Save results as Parquet
    # --------------------------------------------------

    project_root = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "..")
    )

    processed_path = os.path.join(project_root, "data", "processed")

    transformed_df.write.mode("overwrite").parquet(
        f"{processed_path}/sales_transformed"
    )

    monthly_revenue_df.write.mode("overwrite").parquet(
        f"{processed_path}/monthly_revenue"
    )

    category_revenue_df.write.mode("overwrite").parquet(
        f"{processed_path}/category_revenue"
    )

    store_revenue_df.write.mode("overwrite").parquet(
        f"{processed_path}/store_revenue"
    )

    print("\nParquet files saved successfully!")

    spark.stop()


if __name__ == "__main__":
    main()