# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
import requests, schedule, time, re
from utils.utils import query_queue


def extract():
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


if __name__ == "__main__":
    schedule.every(5).seconds.do(extract)
    while True:
        schedule.run_pending()
        time.sleep(2)
        
#TODO: Redo the retry mechanism, no need to read from logging