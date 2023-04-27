from flask import Flask, request, Response, json
import threading
from utils.utils import get_num_workers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, insert
from db_migration.models import RecentSemesterClasses, UsersRegistratedClasses
from config.default import POSTGRES_CONN_STRING

app = Flask(__name__)
app.config.from_object('config.default.DefaultConfig')

@app.route('/getClasses', methods=['GET']) # GET method is used to query all classes from database.
def get_classes():
    engine = create_engine(POSTGRES_CONN_STRING)
    Session = sessionmaker(bind=engine)
    session = Session()
    connection = session.connection()

    classes = connection.execute(select(RecentSemesterClasses)).all()
    classes = [dict(row) for row in classes]

    return Response(json.dumps(classes), mimetype='application/json')