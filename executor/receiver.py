from flask import Flask, request, Response, json
import threading
from executor.invoker import Invoker
from utils.utils import get_num_workers

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, insert
from db_migration.models import RecentSemesterClasses, UsersRegisteredClasses
from config.default import POSTGRES_CONN_STRING

app = Flask(__name__)
app.config.from_object('config.default.DefaultConfig')

engine = create_engine(POSTGRES_CONN_STRING)

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
            'num_worker_requested': len(data['queuedGuids']),
            'num_worker_allocated': len(data['queuedGuids']),          # CHange Worker initialization to the numbers of GUIDs requested
            'invoker_is_alive': invoker_response.is_alive(),
            'invoker_thread_name': invoker_response.getName()
        }
        
        return Response(json.dumps(response_msg), mimetype='application/json')

    elif request.method == 'GET':
        return 'Forbidden', 403
    else:
        return 'Not found', 404


@app.route('/getClasses', methods=['GET']) # GET method is used to query all classes from database.
def get_classes():
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = session.connection()

    classes = connection.execute(select(RecentSemesterClasses)).all()
    classes = [dict(row) for row in classes]

    return Response(json.dumps(classes), mimetype='application/json')

@app.route('/register', methods=['POST']) # POST method is used to register classes.
def register():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = json.loads(request.data)

    query = (insert(UsersRegisteredClasses).
             values(
                    name=data['name'], 
                    cookie=data['cookie'], 
                    classes_registered=data['classes_registered']
                    )
    )
    with session:
        session.execute(query)
        session.commit()
    
    return "Registration Successful"


if __name__ == "__main__":
    app.run(debug=True,
            threaded=True,
            host="0.0.0.0",
            port=5005)
