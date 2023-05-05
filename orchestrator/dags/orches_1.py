from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

# Xcom pull functions
def pull_xcom_init_load(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='create_database')
    if xcom_value == "Sucessfully initialized database and loaded semester data":
        print("Database initialized and semester data loaded")
    else:
        print("XCOM doesn't work")

with DAG(
    "orches_1",

    default_args={
        "owner": "Binh",
        "retries" :1,
        "retry_delay": dates.timedelta(minutes=5),
        "do_xcom_push": True,
    },
    description="Orchestrator",
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
        bash_command = "python -m db_migration.init_load",
        do_xcom_push=True,
    )
    
    check_init_load = PythonOperator(
        task_id = "check_init_load",
        python_callable=pull_xcom_init_load,
    )

    cdc = BashOperator(
        task_id="CDC_for_semester",
        bash_command = "python -m crawler.CDC",
        do_xcom_push=True,
    )

    crawl_classes = BashOperator(
        task_id="crawl_all_classes",
        bash_command = "python -m crawler.classesCrawler",
        do_xcom_push=True,
    )

    crawl_class_details = BashOperator(
        task_id="crawl_details_for_all_classes",
        bash_command = "python -m crawler.detailsCrawler",
    )

    initialize_env >> create_db >> cdc >> crawl_classes >> crawl_class_details

# TODO: use XCOM to add conditions to the DAG