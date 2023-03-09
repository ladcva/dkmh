from db_migration.models import SemesterSnapshot
from crawler.alpha import get_dict_semester_website
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert, update, func
from sqlalchemy.orm import sessionmaker
from datetime import datetime

def init_load():
    # Define the database engine
    engine = create_engine('postgresql+psycopg2://admin:1@localhost:5432/dkmh', echo=False)

    Session = sessionmaker(bind=engine)
    session = Session()

    source_data = get_dict_semester_website()
    set_ids = set(source_data)

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
