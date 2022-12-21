from flask import Flask, request, json
import threading
from executor.invoker import Invoker

app = Flask("ReceiverModule")


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
        
        return str(data)

    elif request.method == 'GET':
        return 'Forbidden', 403
    else:
        return 'Not found', 404


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5005)
