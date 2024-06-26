import requests
import time
import logging
from bs4 import BeautifulSoup
from multiprocessing import Pool
from utils.utils import (
    engine_1,
    DbUtils,
    TempLists,
)
from config.default_logging import setup_logging
from config.default import (
    ASC_AUTH_STR,
    HP_URL,
    LH_URL,
    DEFAULT_NUM_PROCESSES,
    PROCESSES_FACTOR,
)


def crawl_lhp_data(code: str) -> list:
    class_info_list, class_schedule_list = [], []
    cookie = {"ASC.AUTH": ASC_AUTH_STR}
    url = HP_URL.format(latest_sem_id, code, code)
    response = requests.post(url, cookies=cookie)
    soup = BeautifulSoup(response.text, "html.parser")

    for i in range(1, 16):
        try:
            tag = soup.find_all("tr")[i]
            try:
                logging.info("Trying to access data-guidlhp attribute")
                guid = tag["data-guidlhp"]
                logging.info("data-guidlhp attribute accessed successfully")
            except KeyError as e:
                # The data-guidlhp attribute was not found, skip to the next iteration
                logging.error("KeyError occurred, skipping to next iteration", repr(e))
                continue
            span_element = tag.find("span", attrs={"lang": "dkhp-malhp"})
            class_code = (
                span_element.next_sibling.strip().split(" - ")[0].split(": ")[1]
            )
            subject_code = span_element.next_sibling.strip().split(" - ")[1]
            subject_name = soup.find_all("div", class_="name")[0].text
            logging.info(f"Found: {guid}-{class_code}-{subject_code}-{subject_name}")
            class_info_list.append((guid, class_code, subject_code, subject_name))
        except IndexError:
            break

    for item in class_info_list:
        guid = item[0]
        response_2 = requests.post(
            LH_URL, cookies=cookie, data={"GuidIDLopHocPhan": guid}
        )
        soup_2 = BeautifulSoup(response_2.text, "html.parser")
        tag = soup_2.find_all("td")
        schedule = tag[1].text
        room = tag[3].text
        lecturer = tag[6].text
        timeframe = tag[7].text
        class_schedule_list.append((schedule, room, lecturer, timeframe))
    combined_list = [x + y for x, y in zip(class_info_list, class_schedule_list)]
    return combined_list


if __name__ == "__main__":
    setup_logging()
    db_utils = DbUtils(engine_1)
    start_time = time.time()

    # Initialize variables
    temp_instance = TempLists()
    latest_sem_id = db_utils.get_semester_id()[1]  # 0 = newest semester
    class_codes = [item[0] for item in db_utils.get_class_codes()]
    num_processes = DEFAULT_NUM_PROCESSES * PROCESSES_FACTOR  # *3
    chunk_size = (
        len(class_codes) // num_processes
    )  # Determine chunk size for each process

    # Crawl data
    with Pool(processes=num_processes) as p:
        results = p.map(crawl_lhp_data, class_codes, chunksize=chunk_size)
    for result in results:
        temp_instance.add_data(result)
    time.sleep(1)

    # Insert data into database
    logging("Inserting data into classes...")
    db_utils.insert_to_classes(temp_instance.subject_codes)
    logging.info("Data inserted into classes.")

    logging.info("Inserting data into latest semester...")
    db_utils.insert_to_latest_sem(
        guids=temp_instance.guids,
        subject_codes=temp_instance.subject_codes,
        subject_names=temp_instance.subject_names,
        course_codes=temp_instance.course_codes,
        semester_id=latest_sem_id,
        schedules=temp_instance.schedules,
        rooms=temp_instance.rooms,
        lecturers=temp_instance.lecturers,
        timeframes=temp_instance.timeframes,
    )
    logging.info("Data inserted into latest semester.")

    # Results
    end_time = time.time()
    logging.info("The number of classes scheduled is:", len(temp_instance.guids))
    logging.info(f"Processing time: {end_time - start_time - 1} seconds")
    if len(temp_instance.guids) > 0:
        logging.info("Task completed")
    else:
        logging.info("Task failed")
