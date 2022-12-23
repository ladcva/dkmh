from multiprocessing.process import BaseProcess
from random import randrange
from time import sleep
from datetime import datetime


class Worker(BaseProcess):
    """
        This constructor defines tasks that will be executed in the workers.
        """
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def task(cls, identifier, value):

        datetime_now = datetime.now().strftime("%H:%M:%S")
        print(f'Task {identifier} executing with {value} at {datetime_now}', flush=True)

        execution_time = randrange(start=5, stop=14)
        sleep(execution_time)
        print(f"Completed - Task {identifier}")

        return f"({identifier}, {value}) after {execution_time} seconds !"

