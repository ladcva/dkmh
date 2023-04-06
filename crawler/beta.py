import requests, time
from bs4 import BeautifulSoup
from utils.utils import get_semester_id, get_class_codes, insert_to_lastest_sem, insert_to_classes
from config.default import ASC_AUTH_STR, DKHP_URL

def crawl_lhp_data():
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    for code in class_codes:
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
                for item in temp:
                    guid = item[0]
                    specific_class_code = item[1].split(' - ')[0].split(': ')[1]
                    general_class_code = item[1].split(' - ')[1]
                    temp2.append((guid, general_class_code, specific_class_code))
            except IndexError:
                break

if __name__ == "__main__":
    temp = []
    temp2 = []
    guids = []
    subject_codes = []
    course_codes = []
    lastest_sem_id = get_semester_id()[1] # index 1 is for testing purpose, the lastest sem ID doesn't have any codes yet
    class_codes = [item[0] for item in get_class_codes()]
    crawl_lhp_data()
    for each in temp2:
        guids.append(each[0])
        subject_codes.append(each[1])
        course_codes.append(each[2])
    time.sleep(3)
    insert_to_classes(set(subject_codes))
    insert_to_lastest_sem(guids, subject_codes, course_codes)  # Kinda worked, but there is a shit duplicate dont know why figure later
    print("Task completed")



#TODO: Ingest GUID and LHP to database
#TODO: Create a function to check subject availability for the semester, implement retry mechanism
#TODO: When a new semester detected, replace the data in the current RecentSemesterClasses table 
