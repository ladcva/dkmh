from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG(
    "test_orches_1",

    default_args={
        "owner": "Binh",
        "retries" :1,
        "retry_delay": dates.timedelta(minutes=1),

    },
    description="Test DAG",
    schedule=dates.timedelta(days=1),
    start_date=dates.days_ago(2),
    tags=["test"],

)as dag:
    t1 = BashOperator(
        task_id="test_orches_1",
        bash_command="cd /opt/airflow/dkmh && python3 test.py",
    )


