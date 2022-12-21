from jsonrpclib.SimpleJSONRPCServer import SimpleJSONRPCServer
from multiprocessing import Pool
from random import random, randint, randrange
from time import sleep
from datetime import datetime

# num_processes = 15

class Invoker:
    def __init__(self) -> None:
        pass

    def create_wokers():
        pass

    def findlen(*args):

        res = []
        for arg in args:
            try:
                lenval = len(arg)
            except TypeError:
                lenval = None
            res.append((lenval, arg))
        return res

    def f(x):
        return x*x

    def task(self, identifier, value):

        print(f'Task {identifier} executing with {value} at {datetime.now().utcnow()}', flush=True)

        execution_time = randrange(start=5, stop=14)
        sleep(execution_time)
        print(f"Completed - Task {identifier}")
        return f"({identifier}, {value}) after {execution_time} seconds !"

    def invoke_processes(self, **data):
        num_workers = data['workers']
        with Pool(num_workers) as p:
            items = [(i, random()) for i in range(num_workers)]
            result = p.starmap_async(self.task, items)
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
