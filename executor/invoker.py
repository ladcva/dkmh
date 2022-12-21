from multiprocessing import Pool
from random import random
from executor.worker import Worker

NUM_PROCESSES = 15

class Invoker:
    """
    This constructor invokes a pool of parallel workers.
    """
    def __init__(self) -> None:
        pass

    @staticmethod
    def create_wokers():
        pass

    @staticmethod
    def find_len(*args):
        res = []
        for arg in args:
            try:
                lenval = len(arg)
            except TypeError:
                lenval = None
            res.append((lenval, arg))
        return res

    @staticmethod
    def f(x):
        return x*x

    @classmethod
    def invoke_processes(cls, **data):
        num_workers = data['workers']
        with Pool(NUM_PROCESSES) as p:
            items = [(i, random()) for i in range(num_workers)]
            result = p.starmap_async(Worker.task, items)
            for result in result.get():
                print(f'Got result: {result}', flush=True)
            # process pool is closed automatically
            print(f"Successfully run {num_workers} functions asynchronously !")
        return None

    # def main():
    #     server = SimpleJSONRPCServer(('localhost', 3010))
    #     server.register_function(invoke_processes)
    #     print("Start server")
    #     server.serve_forever()
