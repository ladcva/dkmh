from db_migration.models import SemesterSnapshot, base
from crawler.alpha import get_dict_semester_website
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert, update, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database
from config.default import POSTGRES_CONN_STRING
from datetime import datetime

def init_load(engine):

    Session = sessionmaker(bind=engine)
    session = Session()

    source_data = get_dict_semester_website()
    set_ids = set(int(keys) for keys in source_data)

    latest_rec_time = (
        select(func.max(SemesterSnapshot.start_time))
    )

    update_old_rec = (
        update(SemesterSnapshot)
        .where(SemesterSnapshot.start_time == latest_rec_time.scalar_subquery())
        .values(end_time=datetime.now())
        .execution_options(synchronize_session=False)
    )

    insert_new_rec = (
        insert(SemesterSnapshot)
        .values(
            list_semester_id=set_ids,
            details=source_data,
            start_time=datetime.now()
            )
    )

    with session:
        session.execute(update_old_rec)
        session.execute(insert_new_rec)
        session.commit()

if __name__ == '__main__':
    # To create table and database dkmh
    engine = create_engine(POSTGRES_CONN_STRING, echo=False)
    # base.metadata.create_all(engine, checkfirst=True)

    if not database_exists(engine.url):
        create_database(engine.url)
        base.metadata.create_all(engine, checkfirst=True)
        init_load(engine)
    else:
        base.metadata.create_all(engine, checkfirst=True)
        init_load(engine)