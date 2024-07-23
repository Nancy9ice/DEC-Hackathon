from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


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
    task1= BashOperator(
        task_id = 'hackaton_task',
        bash_command= 'python etl_script.py'
     )

    task1 