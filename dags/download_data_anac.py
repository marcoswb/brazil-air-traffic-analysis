from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from controllers.data_controller import DataController

with DAG(
    'download_and_normalize_data_anac',
    description='DAG para baixar e normalizar dados da ANAC',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['download'],
) as dag:
    controller = DataController()

    download_task = PythonOperator(
        task_id='download_data_anac',
        python_callable=controller.download_data_anac,
        provide_context=True
    )

    normalize_task = PythonOperator(
        task_id='normalize_data',
        python_callable=controller.normalize_data,
        provide_context=True
    )

    download_task >> normalize_task
