import requests
# Import necessary db modules
from db_migration.models import SemesterSnapshot, ClassCodesSnapshot, Class, Semester, RecentSemesterClasses
from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker
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
    Session = sessionmaker(bind=engine)
    session = Session()

    semester_ids = session.query(SemesterSnapshot.list_semester_id).filter(SemesterSnapshot.end_time == None).all()[0][0]
    return sorted(semester_ids, reverse=True)

# Import the latest id to class_codes_snapshot table
def insert_latest_id(set_subject_codes):
    Session = sessionmaker(bind=engine)
    session = Session()

    for code in set_subject_codes:
        query = (pg_insert(ClassCodesSnapshot).values(code=code).on_conflict_do_nothing())
        session.execute(query)
    session.commit()

# Get class codes
def get_class_codes():
    Session = sessionmaker(bind=engine)
    session = Session()
    class_codes = session.query(ClassCodesSnapshot.code).all()
    return class_codes

# Insert to RecentSemesterClasses table
def insert_to_latest_sem(guids, subject_codes, subject_names, course_codes, semester_id, schedules, rooms, lecturers, timeframes):
    Session = sessionmaker(bind=engine)
    session = Session()
    data = [{'guid': guid,
            'class_code': subject_code,
            'subject_name': subject_name,
            'course_code': course_code,
            'semester_id': semester_id,
            'time_slot': schedule,
            'room': room,
            'lecturer': lecturer,
            'from_to': timeframe}
            for guid, subject_code, subject_name, course_code, schedule, room, lecturer, timeframe
            in zip(guids, subject_codes, subject_names, course_codes, schedules, rooms, lecturers, timeframes)]
    for row in data:
        query = (pg_insert(RecentSemesterClasses).values(**row).on_conflict_do_nothing())
        session.execute(query)
    session.commit()

# Insert to classes table
def insert_to_classes(subject_codes):
    Session = sessionmaker(bind=engine)
    session = Session()
    
    for code in subject_codes:
        query = (pg_insert(Class).values(code=code).on_conflict_do_nothing())
        session.execute(query)
    session.commit()

def insert_to_semester():
    Session = sessionmaker(bind=engine)
    session = Session()

    details = session.query(SemesterSnapshot.details).filter(SemesterSnapshot.end_time == None).all()[0][0]
    sem_ids = list(details.keys())
    sem_names = list(details.values())
    for sem_id, sem_name in zip(sem_ids, sem_names):
        query = (pg_insert(Semester).values(id=sem_id, name=sem_name).on_conflict_do_nothing())
        session.execute(query)

    session.commit()
        

#TODO: Add DATETIME to insert_to_semester so we can know which is the latest semester

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