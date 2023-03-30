import requests
# Get semester ids in database
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import select
from config.default import POSTGRES_CONN_STRING
from db_migration.models import SemesterSnapshot
# Get constants from config file
from config.default import DEFAULT_NUM_PROCESSES


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



def get_semester_id():
    IDs = []
    engine = create_engine(POSTGRES_CONN_STRING, echo=False)
    query = select(SemesterSnapshot.list_semester_id)
    with engine.connect() as conn:
        IDs.extend(conn.execute(query).fetchall())
    return(IDs[0][0])

