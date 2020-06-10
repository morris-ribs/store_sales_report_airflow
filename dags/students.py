from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.mysql_operator import MySqlOperator

from datacleaner_students import datacleaner_students

yesterday_date = datetime.strftime(datetime.now() - timedelta(1), '%Y-%m-%d')

default_args = {
    'owner': 'Airflow',
    'start_date':  datetime(2020, 6, 9),
    'retries': 1,
    'retry_delay': timedelta(seconds=5)
}

with DAG('students_dag',default_args=default_args,schedule_interval='@daily', template_searchpath=['/usr/local/airflow/sql_files'], catchup=False) as dag:
    t1 = BashOperator(task_id='check_file_exists', bash_command='shasum ~/store_files_airflow/raw_student_data.csv', retries=2, retry_delay=timedelta(seconds=15))

    t2 = PythonOperator(task_id='clean_raw_csv', python_callable=datacleaner_students)

    t3 = MySqlOperator(task_id='create_mysql_table', mysql_conn_id="mysql_conn", sql="create_students_table.sql")

    t4 = MySqlOperator(task_id='insert_into_table', mysql_conn_id="mysql_conn", sql="insert_into_students_table.sql")

    t5 = MySqlOperator(task_id='select_from_table', mysql_conn_id="mysql_conn", sql="select_from_students_table.sql")
   
    t6 = BashOperator(task_id='move_file', bash_command='cat ~/store_files_airflow/students_loaded.csv && mv ~/store_files_airflow/students_loaded.csv ~/store_files_airflow/students_loaded%s.csv' % yesterday_date)
    
    t7 = BashOperator(task_id='rename_raw', bash_command='mv ~/store_files_airflow/raw_student_data.csv ~/store_files_airflow/raw_student_data%s.csv' % yesterday_date)

    t1 >> t2 >> t3 >> t4 >> t5 >> t6 >> t7
