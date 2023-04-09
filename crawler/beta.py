import requests, time
from bs4 import BeautifulSoup
from multiprocessing import Pool
from utils.utils import get_semester_id, get_class_codes, insert_to_lastest_sem, insert_to_classes
from config.default import ASC_AUTH_STR, DKHP_URL, DEFAULT_NUM_PROCESSES

def crawl_lhp_data(code):
    temp = []
    temp2 = []
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    url = DKHP_URL.format(lastest_sem_id, code, code)
    response = requests.post(url, cookies=cookie)
    soup = BeautifulSoup(response.text, 'html.parser')
    for i in range(1, 16):
        try:
            tag = soup.find_all('tr')[i]
            try:
                    print('Trying to access data-guidlhp attribute')
                    attribute = tag['data-guidlhp']
                    print('data-guidlhp attribute accessed successfully')
            except KeyError:
                    # The data-guidlhp attribute was not found, skip to the next iteration
                    print('KeyError occurred, skipping to next iteration')
                    continue
            span_element = tag.find('span', attrs={'lang': 'dkhp-malhp'})
            attribute2 = span_element.next_sibling.strip()
            print(attribute, attribute2)
            temp.append((attribute, attribute2)) 
        except IndexError:
            break
    for item in temp:
        guid = item[0]
        specific_class_code = item[1].split(' - ')[0].split(': ')[1]
        general_class_code = item[1].split(' - ')[1]
        temp2.append((guid, general_class_code, specific_class_code))
    return temp2
if __name__ == "__main__":
    guids = []
    subject_codes = []
    course_codes = []
    lastest_sem_id = get_semester_id()[1] # index 1 is for testing purpose, the lastest sem ID doesn't have any codes yet
    class_codes = [item[0] for item in get_class_codes()]
    chunk_size = len(class_codes) // DEFAULT_NUM_PROCESSES

    with Pool(DEFAULT_NUM_PROCESSES) as p:
        results = p.map(crawl_lhp_data, class_codes, chunksize=chunk_size)
    for result in results:
         for each in result:
            guids.append(each[0])
            subject_codes.append(each[1])
            course_codes.append(each[2])
    time.sleep(3)
    insert_to_classes(subject_codes)
    insert_to_lastest_sem(guids, subject_codes, course_codes)  # Initially worked, needs more testing
    print("Task completed")


#TODO: add Multiprocessing to speed things up -> DONE
#TODO: Ingest GUID and LHP to database -> DONE
#TODO: Create a function to check subject availability for the semester, implement retry mechanism
#TODO: When a new semester detected, replace the data in the current RecentSemesterClasses table 
