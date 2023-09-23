import requests
import logging
import os

# Import necessary db modules
from db_migration.models import (
    SemesterSnapshot,
    ClassCodesSnapshot,
    Class,
    Semester,
    RecentSemesterClasses,
    UsersRegisteredClasses,
)
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, update, and_
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker

# Get constants from config file
from config.default import (
    DEFAULT_NUM_PROCESSES,
    POSTGRES_CONN_STRING,
    POSTGRES_CONN_STRING_SERVER,
)
from dotenv import load_dotenv

load_dotenv(".env")


# Utility functions
def get_num_workers(provided_num_workers):
    try:
        provided_num_workers = int(float(provided_num_workers))
    except TypeError or ValueError:
        print('Invalid value, "workers" must be int.')
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
    soup = BeautifulSoup(main_site.content, "html.parser")

    # Get all <option> tags
    tag_items = soup.select("option[value]")
    if "HK" not in tag_items[1].text:
        print("Invalid cookie, maybe expired ?")
        return False
    else:
        return True


# Create engine_1 for these SQLAlchemy functions
engine_1 = create_engine(POSTGRES_CONN_STRING, echo=False)  # for Airflow
engine_2 = create_engine(
    POSTGRES_CONN_STRING_SERVER, echo=False
)  # for Server and Localhost testing

# Operating Context
OPERATING_ENV = os.environ["ENVIRONMENT"]
if OPERATING_ENV == "dev":
    DEFAULT_ENGINE = engine_2
else:
    DEFAULT_ENGINE = engine_1

# Get the semester ids
def get_semester_id():
    Session = sessionmaker(
        bind=engine_2
    )  # FOR TESTING, change to engine_2 for production
    session = Session()

    semester_ids = (
        session.query(SemesterSnapshot.list_semester_id)
        .filter(SemesterSnapshot.end_time is None)
        .all()[0][0]
    )
    return sorted(semester_ids, reverse=True)


# Import the latest id to class_codes_snapshot table
def insert_latest_id(set_subject_codes):
    Session = sessionmaker(bind=DEFAULT_ENGINE)
    session = Session()

    for code in set_subject_codes:
        query = pg_insert(ClassCodesSnapshot).values(code=code).on_conflict_do_nothing()
        session.execute(query)

    session.commit()


# Get class codes, engine_2 for local testing, change to engine_1 for production
def get_class_codes():
    Session = sessionmaker(bind=DEFAULT_ENGINE)
    session = Session()
    class_codes = session.query(ClassCodesSnapshot.code).all()
    return class_codes


# Insert to RecentSemesterClasses table
def insert_to_latest_sem(**kwargs):
    Session = sessionmaker(bind=DEFAULT_ENGINE)  # engine_2 for testing
    session = Session()

    # Truncate the table before inserting new data
    session.execute("TRUNCATE TABLE recent_semester_classes")

    keys = [
        "guid",
        "class_code",
        "course_code",
        "subject_name",
        "time_slot",
        "room",
        "lecturer",
        "from_to",
    ]
    data = [
        dict(zip(keys, values))
        for values in zip(
            kwargs["guids"],
            kwargs["subject_codes"],
            kwargs["subject_names"],
            kwargs["course_codes"],
            kwargs["schedules"],
            kwargs["rooms"],
            kwargs["lecturers"],
            kwargs["timeframes"],
        )
    ]

    for row in data:
        row["semester_id"] = kwargs["semester_id"]
        query = pg_insert(RecentSemesterClasses).values(**row).on_conflict_do_nothing()
        session.execute(query)

    session.commit()


# Insert to classes table
def insert_to_classes(subject_codes):
    Session = sessionmaker(bind=DEFAULT_ENGINE)  # engine_2 for testing
    session = Session()

    for code in subject_codes:
        query = pg_insert(Class).values(code=code).on_conflict_do_nothing()
        session.execute(query)

    session.commit()


# Insert to semesters table
def insert_to_semester():
    Session = sessionmaker(bind=DEFAULT_ENGINE)
    session = Session()

    details = (
        session.query(SemesterSnapshot.details)
        .filter(SemesterSnapshot.end_time is None)
        .all()[0][0]
    )
    sem_ids = list(details.keys())
    sem_names = list(details.values())
    for sem_id, sem_name in zip(sem_ids, sem_names):
        query = (
            pg_insert(Semester)
            .values(id=sem_id, name=sem_name)
            .on_conflict_do_nothing()
        )
        session.execute(query)

    session.commit()


# Query penultimate Semester Snapshot record to filter out only the lastest Semester
def diff_with_penultimate_semester_snapshot():
    Session = sessionmaker(bind=DEFAULT_ENGINE)  # Change to 1 for prod
    session = Session()

    penultimate_snapshot = (
        session.query(SemesterSnapshot.list_semester_id)
        .order_by(SemesterSnapshot.end_time.desc())
        .offset(1)
        .limit(1)
        .all()[0][0]
    )

    if penultimate_snapshot is not None:
        new_sem = set(get_semester_id()) - set(penultimate_snapshot)
        if new_sem:
            new_sem = new_sem.pop()
            return new_sem
        else:
            return None
    else:
        return None


# Server - side Queries, always is engine_2
def get_semester_id_worker():
    Session = sessionmaker(bind=engine_2)
    session = Session()

    semester_ids = (
        session.query(SemesterSnapshot.list_semester_id)
        .filter(SemesterSnapshot.end_time is None)
        .all()[0][0]
    )
    return sorted(semester_ids, reverse=True)


def query_queue():
    with engine_2.connect() as conn:
        query = select(UsersRegisteredClasses).where(
            UsersRegisteredClasses.status == "pending"
        )
        return conn.execute(query).fetchall()


def update_status(guid, cookie):
    Session = sessionmaker(bind=engine_2)
    session = Session()
    print(f"guid: {guid}")
    print(f"cookie: {cookie}")
    query = (
        update(UsersRegisteredClasses)
        .where(
            and_(
                UsersRegisteredClasses.cookie == cookie,
                UsersRegisteredClasses.guid == guid,
                UsersRegisteredClasses.status == "pending",
            )
        )
        .values(status="processed")
    )
    session.execute(query)
    session.commit()


# TODO: Add DATETIME to insert_to_semester so we can know which is the latest semester


class TempLists:
    def __init__(self):
        self.guids = []
        self.subject_codes = []
        self.subject_names = []
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


# Loggers
# Set up a formatter to include timestamp for logs
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Set up a logger to write logs to a file
file_logger = logging.getLogger("file_logger")
file_logger.setLevel(logging.INFO)
file_handler = logging.FileHandler("executor/logging.log")
file_handler.setFormatter(formatter)
file_logger.addHandler(file_handler)
