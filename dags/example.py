from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Função que será executada pela tarefa
def print_hello():
    print("Hello, Airflow!")
    return "Hello, Airflow!"

# Argumentos padrão para a DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Definindo a DAG
with DAG(
    'test_print_dag',  # Nome único da DAG
    default_args=default_args,
    description='Um DAG simples para testar o Airflow',
    schedule_interval=timedelta(days=1),  # Executa uma vez por dia
    start_date=datetime(2024, 1, 1),
    catchup=False,  # Não executa runs passados
    tags=['teste'],
) as dag:

    # Definindo a tarefa
    print_task = PythonOperator(
        task_id='print_hello_task',
        python_callable=print_hello,
    )

    # Estrutura da pipeline (apenas uma tarefa)
    print_task

# Se quiser adicionar mais tarefas no futuro:
# print_task >> outra_tarefa