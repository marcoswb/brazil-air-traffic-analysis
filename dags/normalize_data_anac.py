from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from controllers.data_controller import DataController

with DAG(
    'normalize_data_anac',
    dag_display_name="2 - Normalizar dados ANAC",
    description='DAG para normalizar dados da ANAC',
    start_date=datetime(2024, 1, 1),
    schedule=None,
    catchup=False,
    tags=['normalize'],
) as dag:
    controller = DataController()

    normalize_task = PythonOperator(
        task_id='normalize_data',
        python_callable=controller.normalize_data,
        provide_context=True
    )

    normalize_task
