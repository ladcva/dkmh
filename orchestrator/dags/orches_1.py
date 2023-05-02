from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
with DAG(
    "test_orches_1",

    default_args={
        "owner": "Binh",
        "retries" :1,
        "retry_delay": dates.timedelta(minutes=5),
        "xcom_push": True,
    },
    description="Test DAG",
    schedule='@daily',
    start_date=dates.days_ago(2),
    tags=["test"],

)as dag:
    initialize_env = BashOperator(
        task_id="activate_environment",
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate",  # Maybe for now we should install all dependencies beforehand and then use this DAG
    )

    create_db = BashOperator(
        task_id="create_database",
        bash_command = "python -m db_migration.create_db",
    )

    cdc = BashOperator(
        task_id="CDC_for_semester",
        bash_command = "python -m crawler.CDC",
    )

    crawl_classes = BashOperator(
        task_id="crawl_all_classes",
        bash_command = "python -m crawler.classesCrawler",
    )

    crawl_class_details = BashOperator(
        task_id="crawl_details_for_all_classes",
        bash_command = "python -m crawler.detailsCrawler",
    )

    initialize_env >> create_db >> cdc >> crawl_classes >> crawl_class_details

# TODO: use XCOM to add conditions to the DAG