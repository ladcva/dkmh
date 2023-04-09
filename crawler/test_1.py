import requests, itertools, time
from config.default import ASC_AUTH_STR, DEFAULT_NUM_PROCESSES
from multiprocessing import Pool
from utils.utils import get_semester_id, insert_latest_id
from functools import partial


available_subject_codes = []

def get_all_subjects():
    list1 = ['INS']
    list2 = range(1, 2)
    list3 = range(0, 200)
    codes = ([f"{i}{j}{k:03d}" for i, j, k in itertools.product(list1, list2, list3)])
    return codes


def validate_subject_code(semester_id, subject_code: str, retry_limit=3, retry_delay=1):
    url = f"https://sv.isvnu.vn/SinhVienDangKy/LopHocPhanChoDangKy?IDDotDangKy={semester_id}&MaMonHoc={subject_code}&DSHocPhanDuocHoc={subject_code}&IsLHPKhongTrungLich=false&LoaiDKHP=1"  #test with a fixed IDDotdangky
    cookie = {'ASC.AUTH': ASC_AUTH_STR}
    
    while retry_limit > 0:
        try:
            response = requests.post(url, cookies=cookie, timeout=5)
            if response.status_code == 200:
                if "lhpchodangky-notfound" in response.text:    # Only return codes that are existed
                    return None
                else:
                    print(f"{subject_code} exists") #fetch the code to database
                    return subject_code
        except Exception as e:
            print(f"{subject_code} - Request exception occurred: {str(e)}")
            time.sleep(retry_delay)
            retry_limit -= 1

    return None


if __name__ == "__main__":
    start_time = time.time()
    codes_list = get_all_subjects()
    semester_ids = get_semester_id()
    num_processes = DEFAULT_NUM_PROCESSES  # Get number of CPU cores available
    chunk_size = len(codes_list) // num_processes  # Determine chunk size for each process

    for semester in semester_ids: # For id in semester ids
        with Pool(processes=num_processes) as pool:
            func = partial(validate_subject_code, semester)   # Create a partial func to pass semester_id to validate_subject_code
            for result in pool.imap_unordered(func, codes_list, chunksize=chunk_size): # Don't need ordered results, so imap_unordered will gain performance
                if result:
                    available_subject_codes.append(result)

        print(available_subject_codes)
        end_time = time.time()
        print(f"Processing time: {end_time - start_time} seconds")
        time.sleep(5)
        
    set_subject_codes = set(available_subject_codes)
    # create_classes_snapshot_table() # Deprecated in next version, ClassesSnapshot table already included in init_load
    insert_latest_id(set_subject_codes)    # Testing insertion to database - worked
    print("Task run sucessfully !")  

 

    
#TODO Refactor and use multiprocessing to speed up the process or think of a better way to optimize the process -> partially done, multiprocessing implemented
#TODO Use a database to store the results
#TODO Get all semester IDs and run the process for each semester ID -- DOING
#TODO Re-design database - Doing
#TODO Implement retry mechanism -> Implemented retry mechanism for ConnectionError - caused by bad internet
#TODO 