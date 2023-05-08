# from flask import Flask, request, Response, json
# import threading
# from executor.invoker import Invoker
# from utils.utils import get_num_workers

# app = Flask("ReceiverModule", root_path='/')

# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5005)

# run.py
from werkzeug.serving import run_simple # werkzeug development server
from executor.receiver import app
if __name__ == '__main__':
    run_simple('0.0.0.0', 5005, app, use_reloader=True, use_debugger=True, use_evalex=True)