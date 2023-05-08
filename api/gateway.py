from flask import Flask, request, Response, json
import threading
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, insert
from db_migration.models import RecentSemesterClasses, UsersRegisteredClasses
from config.default import POSTGRES_CONN_STRING

app = Flask(__name__)
app.config.from_object('config.default.DefaultConfig')
engine = create_engine(POSTGRES_CONN_STRING)

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
            port=5050)

# TODO: Implementing multithreading for the API.
# How to implement multithreading in Flask?
