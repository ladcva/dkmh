import requests
import logging
import os
from dataclasses import dataclass
from db_migration.models import (
    SemesterSnapshot,
    ClassCodesSnapshot,
    Class,
    Semester,
    RecentSemesterClasses,
    UsersRegisteredClasses,
)
from sqlalchemy import create_engine
from sqlalchemy.engine.base import Engine
from sqlalchemy.sql.expression import select, update, and_
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import sessionmaker
from config.default import (
    DEFAULT_NUM_PROCESSES,
    POSTGRES_CONN_STRING,
    POSTGRES_CONN_STRING_SERVER,
)
from config.default_logging import setup_logging
from dotenv import load_dotenv

load_dotenv(".env")
setup_logging()


# Utility functions
def get_num_workers(provided_num_workers):
    try:
        provided_num_workers = int(float(provided_num_workers))
    except TypeError or ValueError:
        logging.info('Invalid value, "workers" must be int.')
        logging.info(f"Using DEFAULT_NUM_PROCESSES={DEFAULT_NUM_PROCESSES} instead.")
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
        logging.error("Invalid cookie, maybe expired ?")
        return False
    else:
        return True


# Create engine_1 for these SQLAlchemy functions
engine_1 = POSTGRES_CONN_STRING  # for Airflow
engine_2 = POSTGRES_CONN_STRING_SERVER  # for local testing
# Operating Context
OPERATING_ENV = os.environ["ENVIRONMENT"]
if OPERATING_ENV == "dev":
    DEFAULT_CONN_STR = POSTGRES_CONN_STRING
else:
    DEFAULT_CONN_STR = POSTGRES_CONN_STRING_SERVER


# New database utility class
class DbUtils:
    def __init__(self, conn_str: str) -> None:
        self.engine = create_engine(conn_str)
        self.session = sessionmaker(bind=self.engine)()

    # Get the semester ids
    def get_semester_id(self) -> list:
        semester_ids = (
            self.session.query(SemesterSnapshot.list_semester_id)
            .filter(SemesterSnapshot.end_time is None)
            .all()[0][0]
        )
        return sorted(semester_ids, reverse=True)

    # Import the latest id to class_codes_snapshot table
    def insert_latest_id(self, set_subject_codes: set) -> None:
        for code in set_subject_codes:
            query = (
                pg_insert(ClassCodesSnapshot).values(code=code).on_conflict_do_nothing()
            )
            self.session.execute(query)

        self.session.commit()

    # Get class codes, engine_2 for local testing, change to engine_1 for production
    def get_class_codes(self) -> list:
        class_codes = self.session.query(ClassCodesSnapshot.code).all()
        return class_codes

    # Insert to RecentSemesterClasses table
    def insert_to_latest_sem(self, **kwargs):

        # Truncate the table before inserting new data
        self.session.execute("TRUNCATE TABLE recent_semester_classes")

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
            query = (
                pg_insert(RecentSemesterClasses).values(**row).on_conflict_do_nothing()
            )
            self.session.execute(query)

        self.session.commit()

    # Insert to classes table
    def insert_to_classes(self, subject_codes: list) -> None:
        for code in subject_codes:
            query = pg_insert(Class).values(code=code).on_conflict_do_nothing()
            self.session.execute(query)

        self.session.commit()

    # Insert to semesters table
    def insert_to_semester(self) -> None:
        details = (
            self.session.query(SemesterSnapshot.details)
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
            self.session.execute(query)

        self.session.commit()

    # Query penultimate Semester Snapshot record to filter out only the lastest Semester
    def diff_with_penultimate_semester_snapshot(self) -> int:
        penultimate_snapshot = (
            self.session.query(SemesterSnapshot.list_semester_id)
            .order_by(SemesterSnapshot.end_time.desc())
            .offset(1)
            .limit(1)
            .all()[0][0]
        )

        if penultimate_snapshot is not None:
            new_sem = set(self.get_semester_id()) - set(penultimate_snapshot)
            if new_sem:
                new_sem = new_sem.pop()
                return new_sem
            else:
                return None
        else:
            return None


# Server - side Queries, always is engine_2
@dataclass
class WebServing:
    engine_2 = create_engine(POSTGRES_CONN_STRING_SERVER, echo=False)
    Session = sessionmaker(engine_2)
    session = Session()

    @classmethod
    def get_semester_id_worker(cls) -> list:  # Int or string idk
        semester_ids = (
            cls.session.query(SemesterSnapshot.list_semester_id)
            .filter(SemesterSnapshot.end_time is None)
            .all()[0][0]
        )
        return sorted(semester_ids, reverse=True)

    @classmethod
    def query_queue(cls) -> list:
        with cls.engine_2.connect() as conn:
            query = select(UsersRegisteredClasses).where(
                UsersRegisteredClasses.status == "pending"
            )
            return conn.execute(query).fetchall()

    @classmethod
    def update_status(cls, guid: str, cookie: str) -> None:
        logging.info(f"guid: {guid}")
        logging.info(f"cookie: {cookie}")
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
        cls.session.execute(query)
        cls.session.commit()


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
