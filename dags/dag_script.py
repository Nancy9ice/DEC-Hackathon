from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dags.etl_script import execute_etl


default_args = {
'owner': 'tj',
'retries': 5,
'retry_delay': timedelta(minutes=2)

}



with DAG(
     dag_id= 'hackaton_dag',
     description='This is our first dag',
     start_date= datetime(2024, 7, 22, 1),
     schedule_interval= '@daily'
        
) as dag: 
    task1= PythonOperator(
        task_id = 'hackaton_task',
        python_callable=execute_etl
     )

    task1 