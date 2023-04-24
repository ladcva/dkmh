# This is the Extractor that will extract the data from the database and send it to the Receiver
# Extractor
from db_migration.models import UsersRegistratedClasses, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert
from config.default import POSTGRES_CONN_STRING
import requests, time, json

# This is the data that is sent through the API Gateway
data = {
    'name': 'Nguyen Van C',
    'cookie': 'FF97FADD11E6A454D89918E7C6B907284ACEC3EE3D63A3E9D40A02537349BB1DE37ACAA2C695E16D0C03BD5A41A3E5AD19EECA01AF80C832A359D2D55F144B13D8F57D3CD006C40C402509D6C8FFA6435B9DD017C0F6449B6486ECAAC7EB3D0C48DBB807D22578C29D8B91B0A82860F5B28D5DB818665886E7A37FCAA45FC8C8',
    'queuedClasses' : ["INS101404","INS101603", "INS101802", "INS106001"]   #Check with the recent semester table to match the GUID - take the class codes out and do queries
}

# Then it get inserted into the database
engine = create_engine(POSTGRES_CONN_STRING, echo=False)
def insert_into_user_regsitered_classes():
    with engine.connect() as conn:
        query = insert(UsersRegistratedClasses).values(name=data['name'], cookie=data['cookie'], classes_registered=data['classes_registered'])
        conn.execute(query)
 
# Then we query the database to get the GUID
def get_guid_from_class_code():
    guid_registered = []
    with engine.connect() as conn:
        for i in range(len(data['queuedClasses'])):
            query = select(RecentSemesterClasses.guid).where(RecentSemesterClasses.course_code == data['queuedClasses'][i])
            guid_registered.append((conn.execute(query).fetchall()[0][0]))
        return guid_registered

# Then combine the GUID with the cookie to send a POST request to the Receiver
data2 = {
    'auth': data['cookie'],
    'workers': 12,
    'queuedGuids': get_guid_from_class_code()
}


# Send a POST request to the Receiver
url = "http://localhost:5005"
requests.post(url, json=data2)
