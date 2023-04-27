import requests
# Import nessary db modules
from db_migration.models import SemesterSnapshot, ClassCodesSnapshot, Class, Semester, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert
from sqlalchemy.dialects.postgresql import insert as pg_insert
# Get constants from config file
from config.default import DEFAULT_NUM_PROCESSES, POSTGRES_CONN_STRING


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

# Create Engine for these SQLAlchemy functions
engine = create_engine(POSTGRES_CONN_STRING, echo=False)

# Get the semester ids
def get_semester_id():
    query = select(SemesterSnapshot.list_semester_id).where(SemesterSnapshot.end_time == None)
    with engine.connect() as conn:
        semester_ids = conn.execute(query).fetchall()[0][0]
    return sorted(semester_ids, reverse=True)

# Import the lastes id to class_codes_snapshot table
def insert_latest_id(set):
    with engine.connect() as conn:
        data = [{'code': item} for item in set]
        conn.execute(insert(ClassCodesSnapshot), data)

# Get class codes
def get_class_codes():
    query = select(ClassCodesSnapshot.code)
    with engine.connect() as conn:
        class_codes = conn.execute(query).fetchall()
    return class_codes

# Insert to RecentSemesterClasses table
def insert_to_lastest_sem(guids, subject_codes, subject_names, course_codes, semester_id, schedules, rooms, lecturers, timeframes):
        with engine.connect() as conn:
            data = [{'guid': guid,
                    'class_code': subject_code,
                    'subject_name': subject_name,
                    'course_code': course_code,
                    'semester_id': semester_id,
                    'time_slot': schedule,
                    'room': room,
                    'lecturer': lecturer,
                    'from_to': timeframe}
                    for guid, subject_code, subject_name, course_code, schedule, room, lecturer, timeframe in zip(guids, subject_codes, subject_names, course_codes, schedules, rooms, lecturers, timeframes)]
            conn.execute(insert(RecentSemesterClasses), data)

# Insert to classes table
def insert_to_classes(subject_codes):
    with engine.connect() as conn:
        data = [{'code': item} for item in set(subject_codes)]
        conn.execute(insert(Class), data)

def insert_to_semester():
    query = select(SemesterSnapshot.details).where(SemesterSnapshot.end_time == None)
    with engine.connect() as conn:
        details = conn.execute(query).fetchall()[0][0]
        sem_ids = list(details.keys())
        sem_names = list(details.values())
        for sem_id, sem_name in zip(sem_ids, sem_names):
            query2 = pg_insert(Semester).values(id=sem_id, name=sem_name).on_conflict_do_nothing()
            conn.execute(query2)

#TODO: Add DATETIME to insert_to_semester so we can know which is the latest semester

#TODO: Decide on_conflict strategy, do nothing or upsert

#TODO: Change Engine execuion to Session execution, with session.connection() to get connection. Using raw Session execution with ORM return instances of classes, rather than database row
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
