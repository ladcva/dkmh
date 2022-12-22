# app.py
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from executor.receiver import app as receiver_app
# from flask_2 import app as flask_app_2
application = DispatcherMiddleware(receiver_app)