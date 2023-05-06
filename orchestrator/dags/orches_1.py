from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator, BranchPythonOperator

# Xcom pull functions
# def determine_next_task_init_load(**kwargs):
#     ti = kwargs['ti']
#     xcom_value = ti.xcom_pull(task_ids='create_database')
#     if xcom_value == "Sucessfully initialized database and loaded semester data":
#         return "cdc"
#     else:
#         return False
    
def determine_next_task_cdc(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='cdc')
    if xcom_value == "Successfully loaded changed data":
        return "crawl_classes"
    else:
        return False

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
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate",  # Manually install dependencies, create Virtual Environment and Create db
    )

    create_db = BashOperator(
        task_id="create_database",
        bash_command = "python -m db_migration.init_load",
        do_xcom_push=True,
    )
    
    # check_init_load = BranchPythonOperator(
    #     task_id = "check_init_load",
    #     python_callable=determine_next_task_init_load,
    #     provide_context=True,
    # )

    cdc = BashOperator(
        task_id="CDC_for_semester",
        bash_command = "python -m crawler.CDC",
        do_xcom_push=True,
    )

    track_cdc = BranchPythonOperator(
        task_id = "track_cdc",
        python_callable=determine_next_task_cdc,
        provide_context=True,
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

    initialize_env >> create_db >> cdc >> track_cdc >> crawl_classes >> crawl_class_details

# TODO: use XCOM to add conditions to the DAG