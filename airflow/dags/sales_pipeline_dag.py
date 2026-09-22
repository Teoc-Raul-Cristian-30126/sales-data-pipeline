from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator


def load_data_to_postgres():
    import sys
    sys.path.insert(0, "/opt/airflow")

    from src.ingestion.load_to_postgres import main
    main()


def upload_data_to_s3():
    import sys
    sys.path.insert(0, "/opt/airflow")

    from src.ingestion.upload_to_s3 import main
    main()


def transform_data_from_s3():
    import sys
    sys.path.insert(0, "/opt/airflow")

    from src.transformations.transform_sales_s3 import main
    main()


def run_dbt():
    import subprocess

    subprocess.run(
        [
            "dbt",
            "run",
            "--project-dir",
            "/opt/airflow/dbt_project",
            "--profiles-dir",
            "/opt/airflow/dbt_project",
        ],
        check=True,
    )


def test_dbt():
    import subprocess

    subprocess.run(
        [
            "dbt",
            "test",
            "--project-dir",
            "/opt/airflow/dbt_project",
            "--profiles-dir",
            "/opt/airflow/dbt_project",
        ],
        check=True,
    )


with DAG(
    dag_id="sales_data_pipeline",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["sales", "data-engineering"],
) as dag:

    load_postgres = PythonOperator(
        task_id="load_data_to_postgres",
        python_callable=load_data_to_postgres,
    )

    upload_s3 = PythonOperator(
        task_id="upload_to_s3",
        python_callable=upload_data_to_s3,
    )

    transform_s3 = PythonOperator(
        task_id="transform_s3",
        python_callable=transform_data_from_s3,
    )

    dbt_run = PythonOperator(
        task_id="dbt_run",
        python_callable=run_dbt,
    )

    dbt_test = PythonOperator(
        task_id="dbt_test",
        python_callable=test_dbt,
    )

    load_postgres >> upload_s3 >> transform_s3 >> dbt_run >> dbt_test