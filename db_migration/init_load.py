from db_migration.models import SemesterSnapshot, base
from crawler.CDC import get_dict_semester_website
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert, update, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from config.default import (
    POSTGRES_CONN_STRING_SERVER,
)  # Change to POSTGRES_CONN_STRING when deploy in prod
from datetime import datetime
from utils.utils import insert_to_semester
import time
import logging


class Initialize:
    def __init__(self, conn_str: str) -> None:
        self.engine = create_engine(conn_str)
        self.init_db()

    def init_db(self):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            base.metadata.create_all(self.engine, checkfirst=True)
            self.init_load()
        else:
            base.metadata.create_all(self.engine, checkfirst=True)
            self.init_load()

        time.sleep(1)
        insert_to_semester()
        logging.info("Sucessfully initialized database and loaded semester data")

    def init_load(self):
        Session = sessionmaker(bind=self.engine)
        session = Session()

        source_data = get_dict_semester_website()
        set_ids = set(int(keys) for keys in source_data)

        latest_rec_time = select(func.max(SemesterSnapshot.start_time))

        update_old_rec = (
            update(SemesterSnapshot)
            .where(SemesterSnapshot.start_time == latest_rec_time.scalar_subquery())
            .values(end_time=datetime.now())
            .execution_options(synchronize_session=False)
        )

        insert_new_rec = insert(SemesterSnapshot).values(
            list_semester_id=set_ids, details=source_data, start_time=datetime.now()
        )

        with session:
            session.execute(update_old_rec)
            session.execute(insert_new_rec)
            session.commit()


if __name__ == "__main__":
    Initialize(POSTGRES_CONN_STRING_SERVER)
