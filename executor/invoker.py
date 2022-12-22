from multiprocessing import Pool
from random import random
from executor.worker import Worker
from utils.utils import get_num_workers


class Invoker:
    """
    This constructor creates a pool of parallel workers.
    """
    def __init__(self) -> None:
        pass

    # @staticmethod
    # def get_num_workers(provided_num_workers):
    #     checked_num_workers: int
    #     try:
    #         checked_num_workers = int(provided_num_workers)
    #     except ValueError or TypeError:
    #         print("Invalid value, \"workers\" must be int.")
    #         print(f"Using DEFAULT_NUM_PROCESSES={DEFAULT_NUM_PROCESSES} instead.")
    #         checked_num_workers = DEFAULT_NUM_PROCESSES
    #     return checked_num_workers

    @staticmethod
    def create_workers(provided_num_workers: int):
        checked_num_workers = get_num_workers(provided_num_workers)
        assert checked_num_workers > 0, f"Number of workers must be greater than 0. Got {checked_num_workers}"

        return Pool(checked_num_workers)

        # if checked_num_workers < DEFAULT_NUM_PROCESSES:
        #     return Pool(checked_num_workers)
        # else:
        #     return Pool(DEFAULT_NUM_PROCESSES)

    @staticmethod
    def find_len(*args):
        res = []
        for arg in args:
            try:
                len_val = len(arg)
            except TypeError:
                len_val = None
            res.append((len_val, arg))
        return res

    @staticmethod
    def f(x):
        return x*x

    @classmethod
    def invoke_processes(cls, **data):
        num_workers_requested = int(data['workers'])

        with cls.create_workers(num_workers_requested) as p:
            items = [(i, random()) for i in range(num_workers_requested)]
            result = p.starmap_async(Worker.task, items)
            for result in result.get():
                print(f'Got result: {result}', flush=True)
            # process pool is closed automatically
            log_message = f"Successfully run {num_workers_requested} functions asynchronously !"
            print(log_message)
        return log_message

    # def main():
    #     server = SimpleJSONRPCServer(('localhost', 3010))
    #     server.register_function(invoke_processes)
    #     print("Start server")
    #     server.serve_forever()
