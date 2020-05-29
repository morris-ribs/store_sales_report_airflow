from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator


default_args = {
    "owner": "Airflow",
    "start_date": datetime(2020, 5, 29),
    "retries": 1,
    "retry_delay": timedelta(seconds=5), # every failed task will be retried within 5 seconds
}

dag = DAG("store_dag", 
    default_args=default_args, schedule_interval='@daily',catchup=False) # catchup false turns off backfilling

# first task is to check whether the file exists or not
t1 = BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/raw_store_transactions.,csv', retry_delay=timedelta(seconds=15, dag=dag)


