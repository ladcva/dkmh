# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
import requests, schedule, time, re
from db_migration.models import UsersRegisteredClasses
from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import select, update
from config.default import POSTGRES_CONN_STRING


# Engine for connecting to the database
engine = create_engine(POSTGRES_CONN_STRING, echo=False)

# Query the Queue
def query_queue():
    with engine.connect() as conn:
        query = select(UsersRegisteredClasses).where(UsersRegisteredClasses.status == 'pending')
        return conn.execute(query).fetchall()

def update_status(guid, cookie):
    Session = sessionmaker(bind=engine)
    session = Session()
    print(f'guid: {guid}')
    print(f'cookie: {cookie}')
    query = update(UsersRegisteredClasses).where(and_(UsersRegisteredClasses.cookie == cookie, UsersRegisteredClasses.guid == guid, UsersRegisteredClasses.status == 'pending')).values(status='processed')
    session.execute(query)
    session.commit()

def job():
    # Combine GUIDs with user's cookie and send a POST request to the Receiver
    url = "http://localhost:5005"

    records = query_queue()
    records.sort(key=lambda record: record.cookie)

    # Group records by cookie, class_code, guid, status into one payload, class codes and guids are lists
    # group these dicts together into a list of dicts

    grouped_record = {}
    for d in records:
        auth = d['cookie']
        status = d['status']
        queued_class = d['class_code']
        queued_guid = d['guid']
    
        grouped_record.setdefault(auth, {'auth': auth, 'status': status, 'queuedClasses': [], 'queuedGuids': []})
        
        grouped_record[auth]['queuedClasses'].append(queued_class)
        grouped_record[auth]['queuedGuids'].append(queued_guid)

    grouped_records = list(grouped_record.values())

    # Send the payload to the Receiver
    for record in grouped_records:
        payload = {
            # 'name': row.name,
            'auth': record['auth'],
            'queuedClasses': record['queuedClasses'],
            'queuedGuids': record['queuedGuids'],
            'status': record['status']
        }

        requests.post(url, json=payload)

    # Read from log file and update the status of the request
    with open('executor/logging.log', 'r') as f:
        for line in f:  # only find in line that is relative to the payload
            match = re.search(r'GUID: (\w+) for user with auth: (\w+)', line)
            if match and "Successfully" in line:
                update_status(match.group(1), match.group(2))
            else:
                continue

if __name__ == "__main__":
    schedule.every(2).seconds.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)
    job()



#TODO - Implement logging
#TODO - make the extractor actively scanning the database for data change
#TODO - write the logic for the extractor
#TODO - track the status of the request and update the database accordingly