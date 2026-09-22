# Sales Data Engineering Pipeline

End-to-end data engineering project built around a synthetic retail sales dataset. The pipeline covers data generation, ingestion, cloud storage, transformation, data warehouse modeling, analytics, orchestration, testing, and CI.

## Tech Stack

* **Python** for data generation and ingestion
* **PostgreSQL** for the source database and data warehouse
* **PySpark** for data transformation
* **Amazon S3** for raw and processed data storage
* **dbt** for SQL transformations and data quality testing
* **Apache Airflow** for workflow orchestration
* **Docker** for containerization
* **GitHub Actions** for continuous integration
* **pytest** for Python tests

## Project Overview

The project simulates a retail data platform.

A synthetic dataset containing products, stores, and sales transactions is generated with Python. The raw data is loaded into PostgreSQL and uploaded to Amazon S3. PySpark is used to process the data, while PostgreSQL provides the dimensional data warehouse used for analytics.

The warehouse follows a star schema with product, store, and date dimensions connected to a sales fact table.

dbt provides the SQL transformation and analytics layer, creating models for monthly, category, and store-level revenue.

Apache Airflow orchestrates the complete workflow, while GitHub Actions runs automated tests and database transformations in CI.

## Dataset

The generated dataset contains:

* 100 products
* 10 stores
* 50,000 sales
* Sales covering 2025
* 8 product categories
* 10 Romanian cities

Product categories:

`Electronics`, `Food`, `Beverages`, `Clothing`, `Home`, `Sports`, `Beauty`, `Books`

The dataset uses a fixed random seed so that it can be reproduced.

## Data Flow

The main pipeline consists of:

**Python → PostgreSQL / S3 → PySpark → Data Warehouse → dbt → Analytics**

Airflow orchestrates the following tasks:

1. Load the generated data into PostgreSQL
2. Upload the raw data to S3
3. Transform the S3 data with PySpark
4. Run dbt models
5. Run dbt tests

## Data Warehouse

The PostgreSQL warehouse uses a star schema.

### Dimensions

**`warehouse.dim_product`**

Contains product information:

* product key
* product ID
* product name
* category

**`warehouse.dim_store`**

Contains store information:

* store key
* store ID
* store name
* city

**`warehouse.dim_date`**

Contains calendar information:

* date key
* full date
* year
* month
* quarter
* day information

### Fact

**`warehouse.fact_sales`**

Contains the sales transactions and measures:

* sale key
* sale ID
* date key
* product key
* store key
* quantity
* unit price
* total amount

## Amazon S3

Raw CSV files are stored under:

```text
s3://sales-data-pipeline-666398468806/raw/
```

The raw dataset contains:

* `products.csv`
* `stores.csv`
* `sales.csv`

PySpark writes processed datasets under:

```text
s3://sales-data-pipeline-666398468806/processed/
```

including:

* sales transformations
* monthly revenue
* category revenue
* store revenue

AWS credentials are supplied through environment variables and are not committed to the repository.

## PySpark

PySpark is used to process the sales data and generate analytical datasets.

The transformations include:

* calculating transaction totals
* aggregating revenue by month
* aggregating revenue by category
* aggregating revenue by store
* writing processed data as Parquet

The Docker environment uses Java 17 for Spark.

## dbt

The dbt project contains three staging models:

* `stg_products`
* `stg_stores`
* `stg_sales`

and three analytical models:

* `monthly_revenue`
* `category_revenue`
* `store_revenue`

The project contains 25 dbt data quality tests covering constraints such as uniqueness, not-null values, and relationships.

## Airflow

The complete pipeline is orchestrated with Apache Airflow.

DAG:

**`sales_data_pipeline`**

The DAG contains five tasks:

* `load_data_to_postgres`
* `upload_to_s3`
* `transform_s3`
* `dbt_run`
* `dbt_test`

The DAG runs inside Docker using Airflow's `LocalExecutor`.

## Testing

Python tests can be executed with:

```bash
pytest tests -v
```

dbt tests:

```bash
dbt test --project-dir dbt_project --profiles-dir dbt_project
```

The project also uses GitHub Actions to run the tests automatically in a clean PostgreSQL environment.

## Docker

The project includes a Docker Compose environment for Airflow and its PostgreSQL metadata database.

Start the environment with:

```bash
docker compose up -d --build
```

Check the running services:

```bash
docker compose ps
```

Airflow is available at:

```text
http://localhost:8080
```

Stop the environment with:

```bash
docker compose down
```

## Running the Pipeline

After starting Docker:

1. Open Airflow at `http://localhost:8080`
2. Open the `sales_data_pipeline` DAG
3. Trigger a DAG run
4. Wait for all five tasks to complete successfully

The pipeline can be run again from the Airflow interface whenever required.

## Example Analytics

The dbt models can be queried directly from PostgreSQL.

### Monthly revenue

```sql
SELECT *
FROM warehouse.monthly_revenue
ORDER BY year, month;
```

### Revenue by category

```sql
SELECT *
FROM warehouse.category_revenue
ORDER BY total_revenue DESC;
```

### Revenue by store

```sql
SELECT *
FROM warehouse.store_revenue
ORDER BY total_revenue DESC;
```

The generated dataset supports analysis of revenue, sales volume, and quantities across time, product categories, and stores.

## CI

GitHub Actions runs the pipeline validation in a clean environment.

The workflow includes:

* dataset generation
* Python tests
* PostgreSQL source table creation
* data loading
* warehouse creation
* dbt connection check
* dbt models
* dbt tests

The workflow runs on pushes and pull requests targeting the `main` branch.

## Running Locally

For local development, install the Python dependencies and configure the required environment variables.

The project uses a `.env` file for local database credentials. AWS credentials are also supplied through environment variables.

The `.env` file is excluded from Git and should never contain credentials that are committed to the repository.

## Results

The current pipeline successfully processes:

* **50,000 sales**
* **100 products**
* **10 stores**
* **365 dates**
* **8 product categories**

The complete Airflow workflow executes successfully from ingestion through dbt testing.

The GitHub Actions CI pipeline also completes successfully with the same warehouse and dbt validation steps.
