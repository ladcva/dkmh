# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
from db_migration.models import UsersRegisteredClasses, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, text
from config.default import POSTGRES_CONN_STRING, DEFAULT_NUM_PROCESSES
import requests, time, json


engine = create_engine(POSTGRES_CONN_STRING, echo=False)

# Query the Queue
def query_queue():
    with engine.connect() as conn:
        query = select(UsersRegisteredClasses)
        return conn.execute(query).fetchall()

# Then we query the database to get the GUID
def get_guid_from_class_code(*args):
    with engine.connect() as conn:
        result = conn.execute(select(RecentSemesterClasses.guid).where(RecentSemesterClasses.course_code.in_(args)))
        guid_registered = result.fetchall()
        return guid_registered


if __name__ == "__main__":
    # Combine GUIDs with user's cookie and send a POST request to the Receiver
    url = "http://localhost:5005"

    for row in query_queue():
        payload = {
            'name': row.name,
            'auth': row.cookie,
            'queuedClasses': row.classes_registered.strip('{}').split(','),
            'queuedGuids': [guid for (guid,) in get_guid_from_class_code(*row.classes_registered.strip('{}').split(','))]
        }
        print(payload)
        requests.post(url, json=payload)



#TODO - Implement logging
