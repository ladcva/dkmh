# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
from db_migration.models import UsersRegistratedClasses, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert
from config.default import POSTGRES_CONN_STRING, DEFAULT_NUM_PROCESSES
import requests, time, json

# This is the data that is sent through the API Gateway
# data = {
#     'name': 'Nguyen Van C',
#     'cookie': 'FF97FADD11E6A454D89918E7C6B907284ACEC3EE3D63A3E9D40A02537349BB1DE37ACAA2C695E16D0C03BD5A41A3E5AD19EECA01AF80C832A359D2D55F144B13D8F57D3CD006C40C402509D6C8FFA6435B9DD017C0F6449B6486ECAAC7EB3D0C48DBB807D22578C29D8B91B0A82860F5B28D5DB818665886E7A37FCAA45FC8C8',
#     'queuedClasses' : ["INS101404","INS101603", "INS101802", "INS106001"]   #Check with the recent semester table to match the GUID - take the class codes out and do queries
# }

# Then it get inserted into the database
engine = create_engine(POSTGRES_CONN_STRING, echo=False)

# def insert_into_user_regsitered_classes():  # This function belongs to the API Gateway
#     with engine.connect() as conn:
#         query = insert(UsersRegistratedClasses).values(name=data['name'], cookie=data['cookie'], classes_registered=data['classes_registered'])
#         conn.execute(query)
 
# Query the Queue
def query_queue():
    with engine.connect() as conn:
        query = select(UsersRegistratedClasses)
        return(conn.execute(query).fetchall())

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
            'workers': DEFAULT_NUM_PROCESSES,
            'queuedGuids': get_guid_from_class_code(row.classes_registered.strip('{}').split(',')[0])[0][0]
        }
        print(payload)
        requests.post(url, json=payload)



#TODO - Implement logging
