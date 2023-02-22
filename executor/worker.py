from multiprocessing.process import BaseProcess
from random import randrange
from time import sleep
from datetime import datetime
from uuid import uuid4


class Worker(BaseProcess):
    """
        This constructor defines tasks that will be executed in the workers.
        """
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def task(cls, auth_user, value):
        task_uuid = uuid4()

        datetime_now = datetime.now().strftime("%H:%M:%S")
        print(f'Task {task_uuid} with object {value} executing at {datetime_now}, auth_user = {auth_user}', flush=True)

        execution_time = randrange(start=3, stop=7)
        sleep(execution_time)
        print(f"Completed - Task {task_uuid}")

        return f"Successfully registered {value['className']} after {execution_time} seconds !"

