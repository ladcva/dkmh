# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
from db_migration.models import UsersRegisteredClasses, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, update
from config.default import POSTGRES_CONN_STRING
import requests, schedule, time


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

def update_status():
    Session = sessionmaker(bind=engine)
    session = Session()
    query = update(UsersRegisteredClasses).where(UsersRegisteredClasses.status == 'pending').values(status='processed')
    session.execute(query)
    session.commit()

def job():
    # Combine GUIDs with user's cookie and send a POST request to the Receiver
    url = "http://localhost:5005"

    for row in query_queue():
        payload = {
            'name': row.name,
            'auth': row.cookie,
            'queuedClasses': row.classes_registered.strip('{}').split(','),
            'queuedGuids': [guid for (guid,) in get_guid_from_class_code(*row.classes_registered.strip('{}').split(','))],
            'status': row.status
        }
        print(payload)
        if payload['status'] == 'pending':
            requests.post(url, json=payload)
            update_status()
            print(payload)
        else:
            continue
        # requests.post(url, json=payload)

if __name__ == "__main__":
    schedule.every(2).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)


    # # Combine GUIDs with user's cookie and send a POST request to the Receiver
    # url = "http://localhost:5005"

    # for row in query_queue():
    #     payload = {
    #         'name': row.name,
    #         'auth': row.cookie,
    #         'queuedClasses': row.classes_registered.strip('{}').split(','),
    #         'queuedGuids': [guid for (guid,) in get_guid_from_class_code(*row.classes_registered.strip('{}').split(','))],
    #         'status': row.status
    #     }
    #     if payload['status'] == 'pending':
    #         requests.post(url, json=payload)
    #         update_status()
    #         print(payload)
    #     else:
    #         continue
    #     requests.post(url, json=payload)



#TODO - Implement logging
#TODO - make the extractor actively scanning the database for data change
#TODO - write the logic for the extractor