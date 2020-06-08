import airflow
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator

args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

DAG = DAG(
  dag_id='simple_xcom',
  default_args=args,
  schedule_interval="@daily",
)

def push_function(**kwargs):
    message='This is the pushed message.'
    ti = kwargs['ti'] # retrieves information about itself reading the value of "ti" from kwargs
    ti.xcom_push(key="message", value=message)

def pull_function(**kwargs):
    ti = kwargs['ti']
    pulled_message = ti.xcom_pull(key='message')
    print("Pulled Message: '%s'" % pulled_message)

t1 = PythonOperator(
    task_id='push_task',
    python_callable=push_function,
    provide_context=True,
    dag=DAG) # push arbitrary message to t2

t2 = PythonOperator(
    task_id='pull_task',
    python_callable=pull_function,
    provide_context=True,
    dag=DAG) # receive message from t1

t1 >> t2

