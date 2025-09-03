from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def print_hello():
    print("Hello, Airflow!")
    return "Hello, Airflow!"

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'test_print_dag',
    default_args=default_args,
    description='Um DAG simples para testar o Airflow',
    catchup=False,
    tags=['teste'],
) as dag:

    print_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello,
    )

    print_task