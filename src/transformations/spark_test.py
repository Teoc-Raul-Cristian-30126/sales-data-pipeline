import os

os.environ["JAVA_HOME"] = r"C:\Users\fery3\.jdks\ms-17.0.20.1"
os.environ["PYSPARK_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"
os.environ["PYSPARK_DRIVER_PYTHON"] = r"D:\DataEngineering\sales-data-pipeline\.venv\Scripts\python.exe"

from pyspark.sql import SparkSession


def main():
    spark = (
        SparkSession.builder
        .appName("SalesDataPipeline")
        .master("local[*]")
        .getOrCreate()
    )

    print("Spark version:", spark.version)

    data = [
        (1, "Laptop", 2500),
        (2, "Mouse", 100),
        (3, "Keyboard", 200),
    ]

    df = spark.createDataFrame(
        data,
        ["id", "product", "price"]
    )

    df.show()

    spark.stop()


if __name__ == "__main__":
    main()