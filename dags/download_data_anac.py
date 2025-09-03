from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import timedelta

from controllers.DataController import DataController

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

controller = DataController()

with DAG(
    'download_and_normalize_data_anac',
    default_args=default_args,
    description='DAG para baixar dados da ANAC',
    catchup=False,
    tags=['download'],
) as dag:

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
