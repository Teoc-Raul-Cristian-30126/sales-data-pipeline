import os

os.environ["JAVA_HOME"] = r"C:\Users\fery3\.jdks\ms-17.0.20.1"
os.environ["PYSPARK_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"

from pyspark.sql import SparkSession


BUCKET_NAME = "sales-data-pipeline-666398468806"


def main():

    spark = (
        SparkSession.builder
        .appName("SparkS3Test")
        .master("local[*]")
        .config(
            "spark.jars.packages",
            "org.apache.hadoop:hadoop-aws:3.4.2,"
            "software.amazon.awssdk:bundle:2.29.52"
        )
        .config(
            "spark.hadoop.fs.s3a.aws.credentials.provider",
            "software.amazon.awssdk.auth.credentials.ProfileCredentialsProvider"
        )
        .getOrCreate()
    )

    print("Reading products.csv from S3...")

    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(f"s3a://{BUCKET_NAME}/raw/products.csv")
    )

    df.show()

    print("Number of products:", df.count())

    spark.stop()


if __name__ == "__main__":
    main()