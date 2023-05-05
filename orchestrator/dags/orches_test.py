from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
with DAG(
    "orches_test",

    default_args={
        "owner": "Binh",
        "retries" :1,
        "retry_delay": dates.timedelta(minutes=5),
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

    def pull_xcom(**kwargs):
        ti = kwargs['ti']
        xcom_value = ti.xcom_pull(task_ids='task1')
        if xcom_value == "Hello World":
            print("XCOM works")
        else:
            print("XCOM doesn't work")

    task2 = PythonOperator(
        task_id = "task2",
        python_callable=pull_xcom,
    )

task1 >> task2