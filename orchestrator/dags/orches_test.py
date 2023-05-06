from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

def determine_next_task(**kwargs):
    ti = kwargs['ti']
    check_output = ti.xcom_pull(task_ids='task1')
    if check_output == 'Hello World':
        return "task2"
    else:
        return False

with DAG(
    "orches_test",

    default_args={
        "owner": "Binh",
        "retries" :1,
        "retry_delay": dates.timedelta(seconds=3),
    },
    description="Test DAG",
    schedule='@daily',
    start_date=dates.days_ago(2),
    tags=["test"],

)as dag:
    task1 = BashOperator(
        task_id="task1",
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate && python test.py",
        do_xcom_push=True,
    )

    task2 = BashOperator(
        task_id="task2",
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate && python test2.py",
    )

    branch_task = BranchPythonOperator(
        task_id='branch_task',
        python_callable=determine_next_task,
        provide_context=True,
    )

    task1 >> branch_task >> task2

