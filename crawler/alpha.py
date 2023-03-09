# Importing libraries
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from utils.utils import sort_by_key

from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select, insert, update, func
from sqlalchemy.orm import sessionmaker
from db_migration.models import SemesterSnapshot
from config.default import POSTGRES_CONN_STRING


def get_dict_semester_website():

    url = 'https://sv.isvnu.vn/dashboard.html'
    headers = {
        'cookie': '_ga=GA1.2.1000091377.1671634543; ASP.NET_SessionId=t0fmbgxgkd3n3ayoutw10p22; __RequestVerificationToken=ixTDUomDQ7f1Kx6DRJzmpedAmS2KmZyjzv8BDV-WFoETIPyuE9nxcEqOTa1PtrNzIX1Kva6rc8WfsPAyNTb9iCZ-aG7X4Bdfu5ZD9ZJvDZ01; PAVWs3tE769MuloUJ81Y=lJVoIW0Nv6nBeFQ5y0RWnLqHyVkRK5V-zGEVZDYbXkY; ASC.AUTH=C755BEDF469030D764CA9EFA3B5F9067E8EB2CECE8C30C1C7365EB0DBBF2725859E0099D6D76321C88CF90ABD53266990D8479247E63757457040F631611FB6DFFF67130DE0A342F3997FE2B30F3ED386EA4680196F761BD1BEE622FD8448C3EA5189E7519ED4BEB7A315283F9430F97D8BF0803E242CC1F4F74C0E4F94F444D; _gid=GA1.2.674121839.1677083976; _gat_gtag_UA_184858033_10=1',
    }

    main_site = requests.get(url, headers=headers)
    soup = BeautifulSoup(main_site.content, 'html.parser')

    # Get all <option> tags
    tag_items = soup.select('option[value]')
    values = [item.get('value') for item in tag_items if item.get('value')]
    text_values = [item.text for item in tag_items if 'HK' in item.text]

    # Convert to dict and sort by key
    dict_res = dict(map(lambda k,v : (k, v), values, text_values))
    dict_res = sort_by_key(dict_res)

    return dict_res

def get_current_semester_detail_db():
    engine = create_engine(POSTGRES_CONN_STRING, echo=True)

    Session = sessionmaker(bind=engine)
    session = Session()
    
    latest_rec_time = (
        select(func.max(SemesterSnapshot.start_time))
    )

    latest_rec_detail = (
        select(SemesterSnapshot.details)
        .where(SemesterSnapshot.start_time == latest_rec_time.scalar_subquery())
    )
    
    with session:
        res = session.execute(latest_rec_detail)
        res = res.fetchone()[0]
        session.commit()
    
    return res
        

def ingest_new_semester():

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


if __name__ == '__main__':
    ids_semester_website = set(int(item) for item in get_dict_semester_website().keys())
    ids_semester_db = set(int(item) for item in get_current_semester_detail_db().keys())

    diff = ids_semester_website - ids_semester_db

    if diff:
        ingest_new_semester()
        print(f'Successfully added semester {diff} to db.')
        # Call beta job
    else:
        print('No changes on website. Latest record in db is already up-to-date.')
