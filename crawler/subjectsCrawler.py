import requests
import itertools
import time
import logging
from config.default import (
    ASC_AUTH_STR,
    NUM_PROCESSES,
    HP_URL,
    POSTGRES_CONN_STRING_SERVER,
)  # Change to POSTGRES_CONN_STRING when deploy in prod
from config.default_logging import setup_logging
from db_migration.init_load import Initialize
from multiprocessing import Pool
from utils.utils import engine_1, DbUtils
from functools import partial

db_utils = DbUtils(engine_1)

semester_ids = db_utils.get_semester_id()
available_subject_codes = []


def get_all_subjects():
    list_1 = [
        "INS",
        "MAT",
        "RUS",
        "PSY",
        "SOC",
        "INE",
        "THL",
        "FIB",
        "PHI",
        "PEC",
        "HIS",
        "POL",
        "INT",
        "FLF",
        "VLF",
        "ENG",
        "LIN",
        "MNS",
        "BSA",
    ]
    list_2 = range(1, 5)
    list_3 = range(0, 500)
    codes = [f"{i}{j}{k:03d}" for i, j, k in itertools.product(list_1, list_2, list_3)]
    return codes


def validate_subject_code(
    semester_id: int, subject_code: str, retry_limit=3, retry_delay=1
):
    url = HP_URL.format(
        semester_id, subject_code, subject_code
    )  # test with a fixed IDDotdangky
    cookie = {"ASC.AUTH": ASC_AUTH_STR}

    while retry_limit > 0:
        try:
            response = requests.post(url, cookies=cookie, timeout=5)
            if response.status_code == 200:
                if "lhpchodangky-notfound" in response.text:
                    return None
                else:
                    logging.info(f"{subject_code} exists")
                    return subject_code
        except Exception as e:
            logging.error(f"{subject_code} - Request exception occurred:", repr(e))
            time.sleep(retry_delay)
            retry_limit -= 1

    return None


def crawl_subject_codes(semester_id: int, codes_list: list, chunk_size: int) -> list:
    available_subject_codes = []
    with Pool(processes=NUM_PROCESSES) as pool:
        func = partial(validate_subject_code, semester_id)
        for result in pool.imap_unordered(func, codes_list, chunksize=chunk_size):
            if result:
                available_subject_codes.append(result)
    return available_subject_codes


if __name__ == "__main__":
    setup_logging()
    # Initialize database
    Initialize(POSTGRES_CONN_STRING_SERVER)

    start_time = time.time()

    codes_list = get_all_subjects()
    chunk_size = len(codes_list) // NUM_PROCESSES
    diff_sem = db_utils.diff_with_penultimate_semester_snapshot()

    if diff_sem:
        available_subject_codes = crawl_subject_codes(diff_sem, codes_list, chunk_size)
    else:
        available_subject_codes = []
        for semester in semester_ids:
            available_subject_codes += crawl_subject_codes(
                semester, codes_list, chunk_size
            )

    logging.info(f"Available subject codes are: {available_subject_codes}")

    time.sleep(1)
    set_subject_codes = set(available_subject_codes)
    db_utils.insert_latest_id(set_subject_codes)
    end_time = time.time()

    logging.info(f"Processing time: {end_time - start_time - 1} seconds")
    logging.info("Task run successfully !")
