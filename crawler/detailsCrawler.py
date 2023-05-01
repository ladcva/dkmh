import requests, time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from utils.utils import get_semester_id, get_class_codes, insert_to_latest_sem, insert_to_classes, TempLists
from config.default import ASC_AUTH_STR, DKHP_URL, LH_URL, DEFAULT_NUM_PROCESSES

def crawl_lhp_data(code):
    temp, temp2, temp3 = [], [], []
    attributes = []
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    url = DKHP_URL.format(latest_sem_id, code, code)
    response = requests.post(url, cookies=cookie)
    soup = BeautifulSoup(response.text, 'html.parser')

    for i in range(1, 16):
        try:
            tag = soup.find_all('tr')[i]
            try:
                    print('Trying to access data-guidlhp attribute')
                    attribute = tag['data-guidlhp']
                    print('data-guidlhp attribute accessed successfully')
                    attributes.append(attribute)
            except KeyError:
                    # The data-guidlhp attribute was not found, skip to the next iteration
                    print('KeyError occurred, skipping to next iteration')
                    continue
            span_element = tag.find('span', attrs={'lang': 'dkhp-malhp'})
            attribute2 = span_element.next_sibling.strip()
            attribute3 = soup.find_all('div', class_='name')[0].text
            print(attribute, attribute2, attribute3)
            temp.append((attribute, attribute2, attribute3)) 
        except IndexError:
            break

    for item in temp:
        guid = item[0]
        specific_class_code = item[1].split(' - ')[0].split(': ')[1]
        general_class_code = item[1].split(' - ')[1]
        subject_name = item[2]
        temp2.append((guid, general_class_code, subject_name, specific_class_code))

    for item in temp2:
        guid = item[0]
        url2= LH_URL
        response2 = requests.post(url2, cookies=cookie, data={'GuidIDLopHocPhan': guid})
        soup2 = BeautifulSoup(response2.text, 'html.parser')
        tag = soup2.find_all('td')
        schedule = tag[1].text
        room = tag[3].text
        lecturer = tag[6].text
        timeframe = tag[7].text
        temp3.append((schedule, room, lecturer, timeframe))
    temp4 = [x + y for x, y in zip(temp2, temp3)]
    return temp4

if __name__ == "__main__":
    temp_instance = TempLists()
    latest_sem_id = get_semester_id()[0] # index 1 is for testing purpose, the latest sem ID doesn't have any codes yet
    class_codes = [item[0] for item in get_class_codes()]
    chunk_size = len(class_codes) // DEFAULT_NUM_PROCESSES

    with Pool(DEFAULT_NUM_PROCESSES) as p:
        results = p.map(crawl_lhp_data, class_codes, chunksize=chunk_size)
    for result in results:
        temp_instance.add_data(result)

    time.sleep(1)
    insert_to_classes(temp_instance.subject_codes)
    insert_to_latest_sem(temp_instance.guids, temp_instance.subject_codes, temp_instance.subject_names, temp_instance.course_codes, latest_sem_id,
                          temp_instance.schedules, temp_instance.rooms, temp_instance.lecturers, temp_instance.timeframes)  # Initially worked, needs more testing
    print("Task completed")

#WARNING: Semester ID in the Semester table has to be imported by hand at the moment, do this if encounter Foreign Key constraint error
#TODO: add Multiprocessing to speed things up -> DONE
#TODO: Ingest GUID and LHP to database -> DONE
#TODO: Create a function to check subject availability for the semester, implement retry mechanism -> Partially done
#TODO: When a new semester detected, replace the data in the current RecentSemesterClasses table
#TODO: Add constraints to subject_names so it can be updated to the classes_snapshot table