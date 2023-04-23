import requests
# Import nessary db modules
from db_migration.models import SemesterSnapshot, ClassCodesSnapshot, Class, Semester, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import Session

# Get constants from config file
from config.default import DEFAULT_NUM_PROCESSES, ASC_AUTH_STR, POSTGRES_CONN_STRING


# Utility functions
def get_num_workers(provided_num_workers):
    try:
        provided_num_workers = int(float(provided_num_workers))
    except TypeError or ValueError:
        print("Invalid value, \"workers\" must be int.")
        print(f"Using DEFAULT_NUM_PROCESSES={DEFAULT_NUM_PROCESSES} instead.")
        provided_num_workers = DEFAULT_NUM_PROCESSES
    finally:
        if provided_num_workers < DEFAULT_NUM_PROCESSES:
            return provided_num_workers
        else:
            return DEFAULT_NUM_PROCESSES

def sort_by_key(unsorted_dict):
    sorted_dict = dict(sorted(unsorted_dict.items()))
    return sorted_dict

def validate_cookie(url, cookie):
    from bs4 import BeautifulSoup

    main_site = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(main_site.content, 'html.parser')

    # Get all <option> tags
    tag_items = soup.select('option[value]')
    if 'HK' not in tag_items[1].text:
        print('Invalid cookie, maybe expired ?')
        return False
    else:
        return True

# Create Session for these SQLAlchemy functions
engine = create_engine(POSTGRES_CONN_STRING, echo=False)
Session = sessionmaker(bind=engine)

# Get semester ids
def get_semester_id():
    semester_ids = []
    with Session() as session:
        query = session.query(SemesterSnapshot.list_semester_id).where(SemesterSnapshot.end_time == None) 
        semester_ids.extend(query.all())
    return(sorted(semester_ids[0][0], reverse=True))

# Import the lastes id to class_codes_snapshot table
def insert_latest_id(set):
    with Session() as session:
        for item in set:
            class_code = item
            insert_new_class_codes = pg_insert(ClassCodesSnapshot).values(code=class_code).on_conflict_do_nothing()
            session.execute(insert_new_class_codes)

# Get class codes from class_codes_snapshot table
def get_class_codes():
    with Session() as session:
        query = select(ClassCodesSnapshot.code)
        class_codes = session.execute(query).fetchall()
    return class_codes

# Insert to recent semester classes table
def insert_to_lastest_sem(guids, subject_codes, subject_names, course_codes, semester_id, schedules, rooms, lecturers, timeframes):
    with Session() as session:
        for i in range(len(guids)):
            insert_lastest_sem = pg_insert(RecentSemesterClasses).values(guid=guids[i], class_code=subject_codes[i], subject_name=subject_names[i],
                                                                    course_code=course_codes[i], semester_id=semester_id, time_slot=schedules[i],
                                                                    room=rooms[i], lecturer=lecturers[i], from_to=timeframes[i]).on_conflict_do_nothing()
            session.add(insert_lastest_sem)
            session.commit()

# Insert to class table
def insert_to_classes(subject_codes):
    with Session() as session:
        for item in set(subject_codes):
            subject_code = item
            insert_classes = pg_insert(Class).values(code=subject_code).on_conflict_do_nothing()
            session.add(insert_classes)
            session.commit()

# Insert to semester table
def insert_to_semester():
    details, sem_ids, sem_names = [], [], []
    with Session() as session:
        query = select(SemesterSnapshot.details).where(SemesterSnapshot.end_time == None)
        details.extend(session.execute(query).fetchall())

    for key,value in details[0][0].items():
        sem_ids.append(key)
        sem_names.append(value)
    
    query2 = pg_insert(Semester).values(id=sem_ids, name=sem_names).on_conflict_do_nothing()
    engine.execute(query2)

#TODO: Add DATETIME to insert_to_semester so we can know which is the latest semester

#TODO: Decide on_conflict strategy, do nothing or upsert

class TempLists:
    def __init__(self):
        self.guids = []
        self.subject_codes = []
        self.subject_names =  []
        self.course_codes = []
        self.schedules = []
        self.rooms = []
        self.lecturers = []
        self.timeframes = []

    def add_data(self, result):
        for each in result:
            self.guids.append(each[0])
            self.subject_codes.append(each[1])
            self.subject_names.append(each[2])
            self.course_codes.append(each[3])
            self.schedules.append(each[4])
            self.rooms.append(each[5])
            self.lecturers.append(each[6])
            self.timeframes.append(each[7])

