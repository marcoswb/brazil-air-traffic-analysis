from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from controllers.load_data_controller import LoadDataController

with DAG(
    'create_db_and_load_data',
    description='DAG para criar banco de dados Postgres e carregar os dados normalizados',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['teste'],
) as dag:
    controller = LoadDataController()

    create_db_task = PythonOperator(
        task_id='create_db',
        python_callable=controller.create_tables,
    )

    load_data_task = PythonOperator(
        task_id='load_data',
        python_callable=controller.load_data,
    )

    create_db_task >> load_data_task