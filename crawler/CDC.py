# Importing libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.utils import sort_by_key, validate_cookie
import logging

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert, update, func
from sqlalchemy.orm import sessionmaker
from db_migration.models import SemesterSnapshot
from config.default import POSTGRES_CONN_STRING, ASC_AUTH_STR, ISVNU_DASHBOARD_URL


def get_dict_semester_website():
    url = ISVNU_DASHBOARD_URL
    cookie = {"ASC.AUTH": ASC_AUTH_STR}

    main_site = requests.get(url, cookies=cookie)
    soup = BeautifulSoup(main_site.content, "html.parser")

    # Get all <option> tags
    tag_items = soup.select("option[value]")
    values = [item.get("value") for item in tag_items if item.get("value")]
    text_values = [item.text for item in tag_items if "HK" in item.text]

    # Convert to dict and sort by key
    dict_res = dict(map(lambda k, v: (k, v), values, text_values))
    dict_res = sort_by_key(dict_res)

    return dict_res


def get_current_semester_detail_db(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    latest_rec_time = select(func.max(SemesterSnapshot.start_time))

    latest_rec_detail = select(SemesterSnapshot.details).where(
        SemesterSnapshot.start_time == latest_rec_time.scalar_subquery()
    )

    with session:
        res = session.execute(latest_rec_detail)
        res = res.fetchone()[0]
        session.commit()

    return res


def ingest_new_semester(engine):
    Session = sessionmaker(bind=engine)
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
    url = ISVNU_DASHBOARD_URL
    cookie = {"ASC.AUTH": ASC_AUTH_STR}

    cookie_is_valid = validate_cookie(url, cookie)

    if cookie_is_valid:
        engine = create_engine(POSTGRES_CONN_STRING, echo=False)

        ids_semester_website = set(
            int(item) for item in get_dict_semester_website().keys()
        )
        ids_semester_db = set(
            int(item) for item in get_current_semester_detail_db(engine).keys()
        )

        diff = ids_semester_website - ids_semester_db

        if diff:
            ingest_new_semester(engine)
            logging.info(f"Found new semester {diff}, added to db.")
            logging.info("Successfully loaded changed data")
            # Call beta job
        else:
            logging.info(
                "No changes on website. Latest record in db is already up-to-date."
            )
