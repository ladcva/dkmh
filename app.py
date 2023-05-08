# app.py
from werkzeug.serving import run_simple
from executor.receiver import app as receiver_app

if __name__ == '__main__':
    run_simple('localhost', 5000, receiver_app,
               use_reloader=True, use_debugger=True, use_evalex=True)