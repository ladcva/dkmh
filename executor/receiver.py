from flask import Flask, request, Response, json
import threading
from executor.invoker import Invoker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, insert
from db_migration.models import RecentSemesterClasses, UsersRegisteredClasses
from config.default import POSTGRES_CONN_STRING_SERVER

# from flask_cors import CORS
from flask_caching import Cache

app = Flask(__name__)
cache = Cache()
cache.init_app(app)
app.config.from_object("config.default.DefaultConfig")
# CORS(app, resources=r'/*')

engine = create_engine(POSTGRES_CONN_STRING_SERVER)


@app.route("/", methods=["POST", "GET"])
def receive_param():
    if request.method == "POST":
        data = json.loads(request.data)
        print(data)

        # no_workers = data['workers']

        invoker = Invoker()
        # invoker_response = invoker.invoke_processes(no_workers=no_workers)
        invoker_response = threading.Thread(
            target=invoker.invoke_processes, name="InvokeAgent", kwargs=data
        )
        invoker_response.start()

        response_msg = {
            "num_worker_requested": len(data["queuedGuids"]),
            "num_worker_allocated": len(data["queuedGuids"]),
            "invoker_is_alive": invoker_response.is_alive(),
            "invoker_thread_name": invoker_response.getName(),
        }

        return Response(json.dumps(response_msg), mimetype="application/json")

    elif request.method == "GET":
        return "Forbidden", 403
    else:
        return "Not found", 404


@app.route(
    "/getClasses", methods=["GET"]
)  # GET method is used to query all classes from database.
@cache.cached(timeout=300)  # Cache the return classes
def get_classes():
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = session.connection()

    classes = connection.execute(select(RecentSemesterClasses)).all()
    classes = [dict(row) for row in classes]

    return Response(json.dumps(classes), mimetype="application/json")


@app.route("/register", methods=["POST"])
def register():
    Session = sessionmaker(bind=engine)
    session = Session()
    data = json.loads(request.data)

    parsed_data = [
        {
            "cookie": data["cookie"],
            "class_code": data["classes_registered"][i],
            "guid": data["guids_registered"][i],
        }
        for i in range(len(data["classes_registered"]))
    ]

    for i in parsed_data:
        query = insert(UsersRegisteredClasses).values(**i)
        session.execute(query)
        session.commit()

    return "Bạn đã đăng ký thành công !"


if __name__ == "__main__":
    app.run(debug=True, threaded=True, host="0.0.0.0", port=5005)
