from flask import Flask, request, Response, json
import threading
from executor.invoker import Invoker
from utils.utils import get_num_workers

app = Flask(__name__)
app.config.from_object('config.default.DefaultConfig')

@app.route('/', methods=['POST', 'GET'])
def receive_param():
    error = None
    if request.method == 'POST':
        data = json.loads(request.data)
        print(data)

        # no_workers = data['workers']

        invoker = Invoker()
        # invoker_response = invoker.invoke_processes(no_workers=no_workers)
        invoker_response = threading.Thread(target=invoker.invoke_processes, name="InvokeAgent", kwargs=data)
        invoker_response.start()

        response_msg = {
            'num_worker_requested': int(float(data['workers'])),
            'num_worker_allocated': get_num_workers(data['workers']),
            'invoker_is_alive': invoker_response.is_alive(),
            'invoker_thread_name': invoker_response.getName()
        }
        
        return Response(json.dumps(response_msg), mimetype='application/json')

    elif request.method == 'GET':
        return 'Forbidden', 403
    else:
        return 'Not found', 404


if __name__ == "__main__":
    app.run(debug=True,
            threaded=True,
            host="0.0.0.0",
            port=5005)
