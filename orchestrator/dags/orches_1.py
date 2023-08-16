from airflow.utils import dates
from airflow import DAG
from airflow.decorators import dag, task
from airflow.operators.bash import BashOperator
from airflow.operators.python import BranchPythonOperator

def determine_next_task_cdc(**kwargs):
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='CDC_for_semester')
    print(xcom_value)
    if xcom_value == "Successfully loaded changed data":
        return "crawl_all_classes"
    else:
        return "crawl_all_classes"      #Change in Production

def determine_next_task_crawl_classes(**kwargs):  
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='crawl_all_classes')
    print(xcom_value)
    if "Task run successfully !" in xcom_value:
        return "crawl_details_for_all_classes"
    else:
        return None

def determine_next_task_portal(**kwargs):  
    ti = kwargs['ti']
    xcom_value = ti.xcom_pull(task_ids='track_portal')
    if "Portal is open" in xcom_value:
        return "activate_extractor"
    else:
        return None

@dag(
    "orches_1",

    default_args={
        "owner": "Binh",
        "retries": 10,
        "retry_delay": dates.timedelta(minutes=5),
    },
    description="Orchestrator",
    schedule='@daily',
    start_date=dates.days_ago(2),
    tags=["orchestrator"],

)   
def dkmh_orchestrator():
    
    @task
    def initialize_env():
        BashOperator(
            task_id="activate_environment",
            bash_command="cd /opt/airflow/dkmh && source venv/bin/activate",  # Manually install dependencies, create Virtual Environment and Create db
        )

    @task
    def create_db():
        BashOperator(
            task_id="create_database",
            bash_command = "cd /opt/airflow/dkmh && python -m db_migration.init_load",
            do_xcom_push=True,
        )
    
    @task
    def cdc(): 
        BashOperator(
            task_id="CDC_for_semester",
            bash_command = "cd /opt/airflow/dkmh && python -m crawler.CDC",
            do_xcom_push=True,
    )

    @task.branch(task_id="track_cdc")
    def determine_next_task_cdc(**kwargs):
        ti = kwargs['ti']
        xcom_value = ti.xcom_pull(task_ids='CDC_for_semester')
        print(xcom_value)
        if xcom_value == "Successfully loaded changed data":
            return "crawl_all_classes"
        else:
            return "crawl_all_classes"
    # track_cdc = BranchPythonOperator(
    #     task_id = "track_cdc",
    #     python_callable=determine_next_task_cdc,
    #     provide_context=True,
    # )

    @task
    def crawl_classes():
        BashOperator( 
            task_id="crawl_all_classes",
            bash_command="cd /opt/airflow/dkmh && python -m crawler.subjectsCrawler",
            do_xcom_push=True,
        )

    @task.branch
    def determine_next_task_crawl_classes(**kwargs):  
        ti = kwargs['ti']
        xcom_value = ti.xcom_pull(task_ids='crawl_all_classes')
        print(xcom_value)
        if "Task run successfully !" in xcom_value:
            return "crawl_details_for_all_classes"
        else:
            return None
        
    # track_crawl_classes = BranchPythonOperator(
    #     task_id = "track_crawl_classes",
    #     python_callable=determine_next_task_crawl_classes,
    #     provide_context=True,
    # )

    @task
    def crawl_class_details():
        BashOperator(
            task_id="crawl_details_for_all_classes",
            bash_command="cd /opt/airflow/dkmh && python -m crawler.detailsCrawler",
        )
    # success -> activate extractor

    @task
    def track_portal(): 
        BashOperator(
            task_id = "track_portal",
            bash_command="cd /opt/airflow/dkmh && python -m utils.portal_tracking",
        )

    @task.branch
    def determine_next_task_portal(**kwargs):  
        ti = kwargs['ti']
        xcom_value = ti.xcom_pull(task_ids='track_portal')
        if "Portal is open" in xcom_value:
            return "activate_extractor"
        else:
            return None
    # track_portal_open = BranchPythonOperator(
    #     task_id = "track_portal_open",
    #     python_callable=determine_next_task_portal,
    #     provide_context=True,
    # )

    @task
    def activate_extractor():
        BashOperator(
            task_id="activate_extractor",
            bash_command="cd /opt/airflow/dkmh && python -m executor.extractor"
        )

    # initialize_env >> create_db >> cdc >> track_cdc >> crawl_classes >> track_crawl_classes >> crawl_class_details >> track_portal >> track_portal_open >> activate_extractor

    initialize_env() >> create_db() >> cdc() >> determine_next_task_cdc() >> crawl_classes() >> determine_next_task_crawl_classes() >> crawl_class_details() >> track_portal() >> determine_next_task_portal() >> activate_extractor()
    
dag = dkmh_orchestrator()