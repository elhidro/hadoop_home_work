from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from random import randint

        
def two_random_int():
    with open('/opt/airflow/dags/file.txt', 'r') as f:
        lines = f.readlines()
    lines = lines[:-1]
    list = [((" ".join(str(x) for x in ([randint(0, 100) for _ in range(2)])))+"\n")]
    res = lines + list 
    with open("/opt/airflow/dags/file.txt", "w") as f:
        f.writelines(res)
        
    
def difference_in_column():
    x = []   
    y = []
    with open("/opt/airflow/dags/file.txt", "r") as f:
        for line in f:
            x.append([int(x) for x in line.split()][0])
            y.append([int(x) for x in line.split()][1])
    r = sum(x)-sum(y)

    with open("/opt/airflow/dags/file.txt", "a") as f:
        f.write(str(r))


#  A DAG represents a workflow, a collection of tasks
with DAG(dag_id="first_dag", start_date=datetime(2022, 12, 1), schedule ="46-50 7 * * *") as dag:

# Tasks are represented as operators
    two_random_int_task = PythonOperator(task_id="two_random_int", python_callable = two_random_int)
    difference_task = PythonOperator(task_id="difference_task", python_callable = difference_in_column)

  #   Set dependencies between tasks

    two_random_int_task >> difference_task