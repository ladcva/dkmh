from airflow.utils import dates
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator


def determine_next_task_cdc(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='cdc')
    print(xcom_value)
    if xcom_value == "Successfully loaded changed data":
        return "crawl_classes"
    else:
        return None

def determine_next_task_crawl_classes(**kwargs):  
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='crawl_classes')
    if xcom_value == "Task completed":
        return "crawl_class_details"
    else:
        return None

def determine_next_task_crawl_classes(**kwargs):  
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='crawl_classes')
    if xcom_value == "Task completed":
        return "crawl_class_details"
    else:
        return False

with DAG(
    "orches_1",

    default_args={
        "owner": "Binh",
        "retries" :10,
        "retry_delay": dates.timedelta(minutes=5),
        "do_xcom_push": True,
    },
    description="Orchestrator",
    schedule='@daily',
    start_date=dates.days_ago(2),
    tags=["orchestrator"],

)as dag:
    initialize_env = BashOperator(
        task_id="activate_environment",
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate",  # Manually install dependencies, create Virtual Environment and Create db
    )

    create_db = BashOperator(
        task_id="create_database",
        bash_command = "cd /opt/airflow/dkmh && python -m db_migration.init_load",
        do_xcom_push=True,
    )
    
    cdc = BashOperator(
        task_id="CDC_for_semester",
        bash_command = "cd /opt/airflow/dkmh && python -m crawler.CDC",
        do_xcom_push=True,
    )

    track_cdc = BranchPythonOperator(
        task_id = "track_cdc",
        python_callable=determine_next_task_cdc,
        provide_context=True,
    )

    track_crawl_classes = BranchPythonOperator(
        task_id = "track_crawl_classes",
        python_callable=determine_next_task_crawl_classes,
        provide_context=True,
    )

    crawl_classes = BashOperator(
        task_id="crawl_all_classes",
        bash_command = "cd /opt/airflow/dkmh && python -m crawler.classesCrawler",
        do_xcom_push=True,
    )

    crawl_class_details = BashOperator(
        task_id="crawl_details_for_all_classes",
        bash_command = "cd /opt/airflow/dkmh && python -m crawler.detailsCrawler",
    )
    # success -> activate extractor
    activate_extractor = BashOperator(
        task_id="activate_extractor",
        bash_command="cd /opt/airflow/dkmh && source venv/bin/activate && python -m executor.extractor"
    )

    initialize_env >> create_db >> cdc >> track_cdc >> crawl_classes >> crawl_class_details >> track_crawl_classes >> activate_extractor

# TODO: use XCOM to add conditions to the DAG