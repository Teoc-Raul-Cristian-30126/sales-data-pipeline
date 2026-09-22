import os

# Java / Python configuration for PySpark
import os

if os.name == "nt":
    os.environ["JAVA_HOME"] = r"C:\Users\fery3\.jdks\ms-17.0.20.1"
    os.environ["PYSPARK_PYTHON"] = (
        r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"
    )
    os.environ["PYSPARK_DRIVER_PYTHON"] = (
        r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"
    )

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, year, month, sum as spark_sum


BUCKET_NAME = "sales-data-pipeline-666398468806"


def main():

    # Create Spark session
    spark = (
        SparkSession.builder
        .appName("SalesDataTransformationS3")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.5.0"
        )
        .config(
            "spark.executor.heartbeatInterval",
            "60s"
        )
        .config(
            "spark.network.timeout",
            "120s"
        )
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    # S3 input paths
    products_path = f"s3a://{BUCKET_NAME}/raw/products.csv"
    stores_path = f"s3a://{BUCKET_NAME}/raw/stores.csv"
    sales_path = f"s3a://{BUCKET_NAME}/raw/sales.csv"

    print("Reading data from S3...")

    # Read CSV files from S3
    products_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(products_path)
    )

    stores_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(stores_path)
    )

    sales_df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(sales_path)
    )

    print(f"Products: {products_df.count()}")
    print(f"Stores: {stores_df.count()}")
    print(f"Sales: {sales_df.count()}")

    # Join sales with products and stores
    transformed_df = (
        sales_df
        .join(products_df, "product_id")
        .join(stores_df, "store_id")
        .withColumn(
            "total_amount",
            col("quantity") * col("unit_price")
        )
        .withColumn(
            "year",
            year(col("sale_date"))
        )
        .withColumn(
            "month",
            month(col("sale_date"))
        )
    )

    print("\nTransformed data:")
    transformed_df.show(10)

    # S3 output directory
    processed_path = f"s3a://{BUCKET_NAME}/processed"

    # ---------------------------------------------------------
    # 1. Transformed sales
    # ---------------------------------------------------------

    sales_transformed_path = f"{processed_path}/sales_transformed"

    transformed_df.write \
        .mode("overwrite") \
        .parquet(sales_transformed_path)

    print(f"Saved transformed sales to: {sales_transformed_path}")

    # ---------------------------------------------------------
    # 2. Monthly revenue
    # ---------------------------------------------------------

    monthly_revenue_df = (
        transformed_df
        .groupBy("year", "month")
        .agg(
            spark_sum("total_amount").alias("total_revenue")
        )
        .orderBy("year", "month")
    )

    monthly_revenue_path = f"{processed_path}/monthly_revenue"

    monthly_revenue_df.write \
        .mode("overwrite") \
        .parquet(monthly_revenue_path)

    print(f"Saved monthly revenue to: {monthly_revenue_path}")

    # ---------------------------------------------------------
    # 3. Category revenue
    # ---------------------------------------------------------

    category_revenue_df = (
        transformed_df
        .groupBy("category")
        .agg(
            spark_sum("total_amount").alias("total_revenue")
        )
        .orderBy(col("total_revenue").desc())
    )

    category_revenue_path = f"{processed_path}/category_revenue"

    category_revenue_df.write \
        .mode("overwrite") \
        .parquet(category_revenue_path)

    print(f"Saved category revenue to: {category_revenue_path}")

    # ---------------------------------------------------------
    # 4. Store revenue
    # ---------------------------------------------------------

    store_revenue_df = (
        transformed_df
        .groupBy("store_id", "store_name", "city")
        .agg(
            spark_sum("total_amount").alias("total_revenue")
        )
        .orderBy(col("total_revenue").desc())
    )

    store_revenue_path = f"{processed_path}/store_revenue"

    store_revenue_df.write \
        .mode("overwrite") \
        .parquet(store_revenue_path)

    print(f"Saved store revenue to: {store_revenue_path}")

    print("\nS3 transformation completed successfully!")

    spark.stop()


if __name__ == "__main__":
    main()